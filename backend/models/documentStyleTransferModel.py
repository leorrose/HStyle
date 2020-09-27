import os
import shutil
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications import vgg19
from PIL import Image
from typing import List, Union, Tuple, Dict


class DocumentStyleTransfer():
    totalVariationWeight:float = 0
    styleWeight:float = 0
    contentWeight:float = 0
    imgNumRows:int = 0
    imgNumCols:int = 0
    ftm:tf.keras.Model = None


    def _preprocessImage(self, imagePath:str) -> tf.Tensor:
        """
        Private Method to open, resize and format pictures into appropriate tensors

        Args:
            image_path (str): the path to image

        Returns:
            tf.Tensor: a tensor representing image
        """
        # load image with content image size
        img:Image.Image  = keras.preprocessing.image.load_img(imagePath, target_size=(self.imgNumCols, self.imgNumCols))
        # create numpy array of image
        img:np.ndarray = keras.preprocessing.image.img_to_array(img)
        # expand to 3d for model
        img:np.ndarray = np.expand_dims(img, axis=0)
        # convert from RGB to BGR, then each color channel is zero-centered with respect to the ImageNet dataset, without scaling.
        img:Union[np.ndarray,tf.Tensor] = vgg19.preprocess_input(img)
        return tf.convert_to_tensor(img)


    def _deprocessImage(self, tns:tf.Tensor) -> tf.Tensor:
        """
        Private Method to convert a tensor into a valid image

        Args:
            tns (tf.Tensor): a tensor from model output

        Returns:
            [tf.Tensor]: a tensor that represents an image
        """
        # reshape to 2d instead of 3d from model output: '(1, 400, 571, 3)' -> '(400, 571, 3)'
        tns:tf.tensor = tns.reshape((self.imgNumCols, self.imgNumCols, 3))
                
        # Remove zero-center by mean pixel
        tns[:, :, 0] += 103.939
        tns[:, :, 1] += 116.779
        tns[:, :, 2] += 123.68
                
        # 'BGR'->'RGB'
        tns:tf.tensor = tns[:, :, ::-1]
        tns:tf.tensor = np.clip(tns, 0, 255).astype("uint8")
                
        # return valid tensor image
        return tns

    def _gramMatrix(self, tns:tf.Tensor) -> tf.Tensor:
        """
        Private Method to calculate gram matrix of an image tensor (feature-wise outer product)

        Args:
            tns (tf.Tensor): a tensor that represents an image

        Returns:
            tf.Tensor: the _gramMatrix result
        """
        # transpose tensor by (2,0,1) for example tensor shape (400, 571, 64)' -> '(64, 400, 571)'
        tns:tf.tensor = tf.transpose(tns, (2, 0, 1))
        # flatten to 2d for example tensor shape '(64, 400, 571)' -> '(64, 228400)'
        features:tf.tensor = tf.reshape(tns, (tf.shape(tns)[0], -1))
        # matrix multiplication of features and features transpose
        gram:tf.tensor = tf.matmul(features, tf.transpose(features))
        return gram

    def _styleLoss(self, style:tf.Tensor, combination:tf.Tensor) -> float:
        """
        Private Method to calculate the style loss. 
        The "style loss" is designed to maintain the style of the reference image in the generated image.
        It is contentd on the gram matrices (which capture style) of feature maps from the style reference image
        and from the generated image.

        Args:
            style (tf.Tensor): tensor representing style image
            combination (tf.Tensor): tensor representing combination image

        Returns:
            float: the loss value
        """
        # calc gram matrix for style
        style_gramMatrix:tf.tensor = self._gramMatrix(style)
        # calc gram matrix for combination
        combination_gramMatrix:tf.tensor = self._gramMatrix(combination)
        # image depth
        channels:int = 3
        # image size
        size:int = self.imgNumCols * self.imgNumCols
        # MSE loss between gram matrix of input and the style image
        return tf.reduce_sum(tf.square(style_gramMatrix - combination_gramMatrix)) / (4.0 * (channels ** 2) * (size ** 2))

    def _contentLoss(self, content:tf.Tensor, combination:tf.Tensor) -> float:
        """
        Private Method to calculate the content loss. 
        An auxiliary loss function designed to maintain the "content" of the
        content image in the generated image.

        Args:
            content (tf.Tensor): tensor representing the content content image
            combination (tf.Tensor): tensor representing combination image

        Returns:
            float: the loss value
        """
        # MSE loss between the content content image’s features and the combination image’s features
        return tf.reduce_sum(tf.square(combination - content))
        
    def _totalVariationLoss(self, tns:tf.Tensor) -> float:
        """
        Private Methos to calculate total variation loss (a regularization loss), designed to keep the generated image locally coherent.

        Args:
            tns (tf.Tensor):  tensor representing the generated image

        Returns:
            float: the loss value
        """
        a:tf.Tensor = tf.square(tns[:, : self.imgNumCols - 1, : self.imgNumCols - 1, :] - tns[:, 1:, : self.imgNumCols - 1, :])
        b:tf.Tensor = tf.square(tns[:, : self.imgNumCols - 1, : self.imgNumCols - 1, :] - tns[:, : self.imgNumCols - 1, 1:, :])
        return tf.reduce_sum(tf.pow(a + b, 1.25))

    def _featureExtractorModel(self) -> tf.keras.Model:
        """
        Private Method to create a model that returns the activation values for every layer in VGG19 (as a dict)

        Returns:
            tf.keras.Model: a model that returns the activation values for every layer in VGG19 (as a dict)
        """
        # Build a VGG19 model loaded with pre-trained ImageNet weights
        model:tf.keras.Model = vgg19.VGG19(weights="imagenet", include_top=False)

        # Get the symbolic outputs of each "key" layer (they have unique names)
        outputsDict:Dict[str, tf.Tensor] = dict([(layer.name, layer.output) for layer in model.layers])

        # Set up a model that returns the activation values for every layer in VGG19 (as a dict).
        featureExtractor:tf.keras.Model = keras.Model(inputs=model.inputs, outputs=outputsDict)
        return featureExtractor

    def _computeLoss(self, combinationImage:tf.Tensor, contentImage:tf.Tensor, styleReferenceImage:tf.Tensor) -> float:
        """
        Private Method to combine style, content, total variation loss functions  into one loss function for model evaluation.

        Args:
            combinationImage (tf.Tensor): 
            contentImage (tf.Tensor): 
            styleReferenceImage (tf.Tensor):

        Returns:
            float: the loss value
        """
        # List of layers to use for the style loss.
        styleLayerNames:List[str] = ["block1_conv1", "block2_conv1", "block3_conv1", "block4_conv1", "block5_conv1"]
        
        # The layer to use for the content loss.
        contentLayerName:str = "block5_conv2"

        # concat all images to one for model prediction
        inputTensor:tf.Tensor = tf.concat([contentImage, styleReferenceImage, combinationImage], axis=0)
            
        # get prediction from model with input image as a dict of each layer
        features:Dict[str, tf.Tensor]  = self.ftm(inputTensor)

        # Initialize the loss
        loss:np.ndarray = tf.zeros(shape=())

        # get content layer
        layerFeatures = features[contentLayerName] 
        # get content image features from layer prediction
        contentImageFeatures = layerFeatures[0, :, :, :]
        # get combination image features from layer prediction
        combinationFeatures = layerFeatures[2, :, :, :]
        # add content loss to total loss
        loss:np.ndarray = loss + self.contentWeight * self._contentLoss(contentImageFeatures, combinationFeatures)

        # Add style loss
        for layerName in styleLayerNames:
            # get style layer 
            layerFeatures = features[layerName]
            # get style image features from layer prediction
            styleReferenceFeatures = layerFeatures[1, :, :, :]
            # get combination image features from layer prediction
            combinationFeatures = layerFeatures[2, :, :, :]
            # add style loss to total loss
            loss += (self.styleWeight / len(styleLayerNames)) * self._styleLoss(styleReferenceFeatures, combinationFeatures)

        # Add total variation loss
        loss += self.totalVariationWeight * self._totalVariationLoss(combinationImage)
        return loss

    @tf.function
    def _computeLossAndGrads(self, combinationImage:tf.Tensor, contentImage:tf.Tensor, styleReferenceImage:tf.Tensor) -> Tuple[float, tf.Tensor]:
        """
        Method to compile loss function to make it faster.

        Args:
            combinationImage (tf.Tensor): 
            contentImage (tf.Tensor): 
            styleReferenceImage (tf.Tensor): 

        Returns:
            Tuple[float, tf.Tensor]: 
        """
        with tf.GradientTape() as tape:
            loss:float = self._computeLoss(combinationImage, contentImage, styleReferenceImage)
        grads:tf.Tensor = tape.gradient(loss, combinationImage)
        return loss, grads

    def renderImage(self, contentImgPath:str, styleImgPath:str, resultPrefix:str = 'result', resultsDir:str = './', totalVariationWeight:float = 1e-6,
                    styleWeight:float = 1e-6, contentWeight:float = 2.5e-8) -> None:
        """[summary]

        Args:
            contentImgPath (str): our content image path
            styleImgPath (str): our style image path
            resultPrefix (str, optional): the result prefix for saving images and content. Defaults to 'result-'.
            resultsDir (str, optional): directory to save content. Defaults to './'.
            totalVariationWeight (float, optional): total variation loss weight. Defaults to 1e-6.
            styleWeight (float, optional): style loss weight. Defaults to 1e-6.
            contentWeight (float, optional): content loss weight. Defaults to 2.5e-8.
        """
        # create directory for results
        if os.path.exists(resultsDir):
            shutil.rmtree(resultsDir)
        os.mkdir(resultsDir)

        # Weights of the different loss components
        self.totalVariationWeight:float = totalVariationWeight
        self.styleWeight:float = styleWeight
        self.contentWeight:float = contentWeight

        # Dimensions of the generated picture.
        width, height = keras.preprocessing.image.load_img(contentImgPath).size
        self.imgNumCols:int = 400
        self.imgNumCols:int = int(width * self.imgNumCols / height)

        # create feature extractor model
        self.ftm = self._featureExtractorModel()

        # set model optimizer
        optimizer = keras.optimizers.SGD(keras.optimizers.schedules.ExponentialDecay(initial_learning_rate=100.0, decay_steps=100, decay_rate=0.96))

        # get content image
        contentImage = self._preprocessImage(contentImgPath)
        # get style image
        styleReferenceImage = self._preprocessImage(styleImgPath)
        # create combination initial image
        combinationImage = tf.Variable(self._preprocessImage(contentImgPath))

        # set number of iteration of model
        iterations = 4000
        for i in range(1, iterations + 1):
            # compute loss and gradient
            loss, grads = self._computeLossAndGrads(combinationImage, contentImage, styleReferenceImage)
            # apply the gradient to combination image
            optimizer.apply_gradients([(grads, combinationImage)])
            # for each 50 iteration ouput results
            if i % 50 == 0:
                print("Iteration %d: loss=%.2f" % (i, loss))
                img = self._deprocessImage(combinationImage.numpy())
                fname = resultsDir + '/' + resultPrefix + f"_at_iteration_{i}.png"
                keras.preprocessing.image.save_img(fname, img)
