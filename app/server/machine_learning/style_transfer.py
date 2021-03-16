
"""
Style transfer model
"""


import numpy as np
import tensorflow as tf
from typing import List, Dict, Tuple
from PIL import Image


def load_img(img: np.ndarray) -> tf.Tensor:
    """
    Function to load an image and limit its maximum dimension to 512 pixels

    Args:
      img (np.ndarray): an rgb image

    Returns:
      tf.Tensor: a tensor that represents an image
    """
    # set max dimensions
    max_dim: int = 512
    # convert to float, each val between [0,1]
    img: tf.Tensor = tf.convert_to_tensor(img, dtype=tf.float32)
    img /= 255
    # get image width and height
    shape: tf.Tensor = tf.cast(tf.shape(img)[:-1], tf.float32)
    # get max height or width
    long_dim: tf.Tensor = max(shape)
    # get the ratio scale to 512
    scale: tf.Tensor = max_dim / long_dim
    # get the new image shape by scale ratio
    new_shape: tf.Tensor = tf.cast(shape * scale, tf.int32)
    # resize image
    img: tf.Tensor = tf.image.resize(img, new_shape)
    # expand dimension to image array
    img: tf.Tensor = img[tf.newaxis, :]
    return img


def tensor_to_image(tensor: tf.Tensor) -> Image:
    """
    function to transform tensor to an image

    Args:
      tensor (tf.Tensor): tensor representing image

    Returns:
      PIL.Image: pillow image object
    """
    # multiply by 255 to undo normalization
    tensor = tensor*255
    # turn to array
    tensor: np.ndarray = np.array(tensor, dtype=np.uint8)
    # remove the array dimension, leave only image
    if np.ndim(tensor) > 3:
        assert tensor.shape[0] == 1
        tensor: tf.Tensor = tensor[0]
    # return array from image
    return Image.fromarray(tensor)


def vgg_layers(layer_names: List[str]) -> tf.keras.Model:
    """
    Method to Creates a vgg model that returns a list of intermediate output
    values.

    Args:
      layer_names (list[str]): intermediate layer names for output

    Returns:
       tf.keras.Model: a vgg model that returns a list of intermediate
       output values
    """
    # Load pretrained VGG, trained on imagenet data
    vgg: tf.keras.Model = tf.keras.applications.VGG19(include_top=False,
                                                      weights='imagenet')
    # set layers to not be trained
    vgg.trainable = False

    # get the outputs of each intermediate layer
    outputs = [vgg.get_layer(name).output for name in layer_names]

    # return functional API
    return tf.keras.Model([vgg.input], outputs)


def gram_matrix(input_tensor: tf.Tensor) -> tf.Tensor:
    """
    Function to calculate gram matrix of an image (feature-wise outer product)

    Args:
      input_tensor (tf.Tensor): the image

    Returns:
      tf.Tensor: the gram matrix result
    """
    # calculate the outer product of the feature vector with itself
    # at each location
    result: tf.Tensor = tf.linalg.einsum('bijc,bijd->bcd', input_tensor,
                                         input_tensor)

    # get tensor shape
    input_shape: tf.Tensor = tf.shape(input_tensor)

    # calculate shape to avarge outer product
    num_locations: tf.Tensor = tf.cast(
        input_shape[1]*input_shape[2], tf.float32)

    # return averaging outer product over all locations
    return result/(num_locations)


class StyleContentModel(tf.keras.models.Model): # pylint: disable=W0223
    """
    Class to get the content and style from model
    """
    def __init__(self, style_layers: List[str], content_layers: List[str]):
        """
        Initialization Method

        Args:
          style_layers (List[str]): the style intermidate layers
          content_layers (List[str]): the content intermidate layers
        """

        super(StyleContentModel, self).__init__()
        self.vgg: tf.keras.Model = vgg_layers(style_layers + content_layers)
        self.vgg.trainable = False
        self.style_layers: List[str] = style_layers
        self.num_style_layers: int = len(style_layers)
        self.content_layers: List[str] = content_layers

    def call(self, inputs: tf.Tensor) -> Dict[str, tf.Tensor]: # pylint: disable=W0221
        """
        Method to overide call operation to enable creation of gram matrix
        and content

        Args:
          inputs (tf.Tensor): a tensor that represents content ans style
          images, Expects float input in [0,1]

        Returns:
          Dict[str, Union[list, Tensor]]: gram matrix of the style layers and
          content of the content layers:
        """
        # make image in range [0, 255]
        inputs: tf.Tensor = inputs*255.0

        # vgg19 preprocess function
        preprocessed_input: tf.Tensor = tf.keras.applications.\
            vgg19.preprocess_input(inputs)

        # forward pass content and style images
        outputs: List[tf.Tensor] = self.vgg(preprocessed_input)

        # get the outputs of content and style from the forward pass
        style_outputs, content_outputs = (outputs[:self.num_style_layers],
                                          outputs[self.num_style_layers:])

        # calculate gram matrix for style outputs
        style_outputs: List[tf.Tensor] = [gram_matrix(style_output)
                                          for style_output in style_outputs]

        # create dict where key is layer name and value is output
        content_dict = {content_name: value
                        for content_name, value # pylint: disable=R1721
                        in zip(self.content_layers, content_outputs)}

        # create dict where key is layer name and value is output
        style_dict = {style_name: value
                      for style_name, value # pylint: disable=R1721
                      in zip(self.style_layers, style_outputs)}

        return {'content': content_dict, 'style': style_dict}


def style_content_loss(outputs: Dict[str, tf.Tensor], style_targets: tf.Tensor,
                       content_targets: tf.Tensor, num_style_layers: int,
                       num_content_layers: int, style_weight: float,
                       content_weight: float) -> tf.Tensor:
    """
    Function to calculate style and content loss

    Args:
      outputs (Dict[str, tf.Tensor]): the rendered image intermidate outputs
      style_targets (tf.Tensor): the style intermidate outputs
      content_targets (tf.Tensor): the content intermidate outputs
      num_style_layers: number of style layers
      num_content_layers(int): number of content layers
      style_weight (float): the style weight
      content_weight (float): the content weight

    Returns:
      tf.Tensor: style and content loss
    """
    # get style intermidate outputs of rendered image
    style_outputs: tf.Tensor = outputs['style']

    # get content intermidate outputs of rendered image
    content_outputs: tf.Tensor = outputs['content']

    # calculate style loss
    style_loss: tf.Tensor = tf.add_n(
        [tf.reduce_mean((style_outputs[name]-style_targets[name])**2)
         for name in style_outputs.keys()])
    style_loss *= style_weight / num_style_layers

    # calculate content loss
    content_loss: tf.Tensor = tf.add_n(
        [tf.reduce_mean((content_outputs[name]-content_targets[name])**2)
         for name in content_outputs.keys()])
    content_loss *= content_weight / num_content_layers

    # return style and content loss
    return style_loss + content_loss


def clip_0_1(image: tf.Tensor) -> tf.Tensor:
    """
    Method to keep the pixel values between 0 and 1

    Args:
        inputs (tf.Tensor): the image

    Returns:
         tf.Tensor: a clipped tensor
    """
    return tf.clip_by_value(image, clip_value_min=0.0, clip_value_max=1.0)


def train_step_without_variation_loss(image: tf.Variable,
                                      extractor: StyleContentModel,
                                      opt: tf.optimizers.Adam,
                                      style_targets: tf.Tensor,
                                      content_targets: tf.Tensor,
                                      num_style_layers: int,
                                      num_content_layers: int,
                                      style_weight: float,
                                      content_weight: float) -> None:
    """
    Method to apply a training step with total variation consideration

    Args:
      image (tf.Variable): the rendered image
      extractor (StyleContentModel): the intermidate layer extractor
      opt (tf.optimizers.Adam): the optimizer
      style_targets (tf.Tensor): the style intermidate outputs
      content_targets (tf.Tensor): the content intermidate outputs
      num_style_layers: number of style layers
      num_content_layers(int): number of content layers
      style_weight (float): the style weight
      content_weight (float): the content weight
      total_variation_weight (float): the total variation weight
    """
    with tf.GradientTape() as tape:
        # forward pass rendered image
        outputs: Dict[str, tf.Tensor] = extractor(image)

        # calculate style content loss
        loss: tf.Tensor = style_content_loss(outputs, style_targets,
                                             content_targets, num_style_layers,
                                             num_content_layers, style_weight,
                                             content_weight)

    # calculate gradient descent
    grad = tape.gradient(loss, image)

    # apply gradient descent
    opt.apply_gradients([(grad, image)])

    # update image and clip to [0,1]
    image.assign(clip_0_1(image))


def high_pass_x_y(image: tf.Variable) -> Tuple[tf.Tensor, tf.Tensor]:
    """
    Method to calc high frequency components of the image on x axis
    and y axis of image

    Args:
      image (tf.Variable): the rendered image

    Returns:
      Tuple[tf.Tensor, tf.Tensor]: high frequency components of the image
    """
    x_var: tf.Tensor = image[:, :, 1:, :] - image[:, :, :-1, :]
    y_var: tf.Tensor = image[:, 1:, :, :] - image[:, :-1, :, :]
    return x_var, y_var


def total_variation_loss(image: tf.Variable) -> tf.Tensor:
    """
    Method to calc total variation loss

    Args:
      image (tf.Variable): the rendered image

    Returns:
      tf.Tensor: the total variation
    """
    x_deltas, y_deltas = high_pass_x_y(image)
    return tf.reduce_sum(tf.abs(x_deltas)) + tf.reduce_sum(tf.abs(y_deltas))


def train_step_with_variation_loss(image: tf.Variable,
                                   extractor: StyleContentModel,
                                   opt: tf.optimizers.Adam,
                                   style_targets: tf.Tensor,
                                   content_targets: tf.Tensor,
                                   num_style_layers: int,
                                   num_content_layers: int,
                                   style_weight: float,
                                   content_weight: float,
                                   total_variation_weight: float) -> None:
    """
    Method to apply a training step with total variation consideration

    Args:
      image (tf.Variable): the rendered image
      extractor (StyleContentModel): the intermidate layer extractor
      opt (tf.optimizers.Adam): the optimizer
      style_targets (tf.Tensor): the style intermidate outputs
      content_targets (tf.Tensor): the content intermidate outputs
      num_style_layers: number of style layers
      num_content_layers(int): number of content layers
      style_weight (float): the style weight
      content_weight (float): the content weight
      total_variation_weight (float): the total variation weight
    """
    with tf.GradientTape() as tape:
        # forward pass rendered image
        outputs: Dict[str, tf.Tensor] = extractor(image)

        # calculate style content loss
        loss: tf.Tensor = style_content_loss(outputs, style_targets,
                                             content_targets, num_style_layers,
                                             num_content_layers, style_weight,
                                             content_weight)

        # add total variation loss
        loss += total_variation_weight*tf.image.total_variation(image)

    # calculate gradient descent
    grad = tape.gradient(loss, image)

    # apply gradient descent
    opt.apply_gradients([(grad, image)])

    # update image and clip to [0,1]
    image.assign(clip_0_1(image))


def render_image(content_image: np.ndarray, style_image: np.ndarray,
                 content_layers: List[str], style_layers: List[str],
                 style_weight: float, content_weight: float,
                 total_variation_weight: float, epochs_without_variation: int,
                 epochs_with_variation: int, steps_per_epoch: int) -> Image:
    """
    Method to render neural style transfer from style and content

    Args:
      content_image (np.ndarray): the content image
      style_image (np.ndarray): the style image
      content_layers (List[str]): the conten intermediate layers
      style_layers (List[str]): the style intermediate layers
      style_weight (float): the style weight
      content_weight (float): the content weight
      total_variation_weight (float): the total variation weight
      epochs_without_variation (int): number of epochs to perform without
      total variation consideration
      epochs_with_variation(int): number of epochs to perform with
      total variation consideration
      steps_per_epoch(int): number of steps in each epoch

    Returns:
      Image: the rendered image
    """
    # calculate number of content and style layers
    num_content_layers: int = len(content_layers)
    num_style_layers: int = len(style_layers)

    # load content and style images
    content_image: tf.Tensor = load_img(content_image)
    style_image: tf.Tensor = load_img(style_image)

    # create extractor
    extractor: StyleContentModel = StyleContentModel(style_layers,
                                                     content_layers)
    # get style content outputs
    style_targets: tf.Tensor = extractor(style_image)['style']
    content_targets: tf.Tensor = extractor(content_image)['content']

    # create optimizer for gradient decent
    opt: tf.optimizers.Adam = tf.optimizers.Adam(learning_rate=0.02,
                                                 beta_1=0.99, epsilon=1e-1)

    # define a tf.Variable to contain the image to optimize
    image: tf.Variable = tf.Variable(content_image)

    # perform optimization without total variation
    step: int = 0
    for _ in range(epochs_without_variation):
        for _ in range(steps_per_epoch):
            step += 1
            train_step_without_variation_loss(image, extractor, opt,
                                              style_targets, content_targets,
                                              num_style_layers,
                                              num_content_layers, style_weight,
                                              content_weight)

    # define a tf.Variable to contain the image to optimize
    image: tf.Variable = tf.Variable(content_image)

    # perform optimization with total variation
    step: int = 0
    for _ in range(epochs_with_variation):
        for _ in range(steps_per_epoch):
            step += 1
            train_step_with_variation_loss(image, extractor, opt,
                                           style_targets, content_targets,
                                           num_style_layers,
                                           num_content_layers, style_weight,
                                           content_weight,
                                           total_variation_weight)
    return tensor_to_image(image)
