import os
import shutil
import numpy as np
import tensorflow as tf
from typing import List
from PIL import Image

# best intermediate layers for content representation
content_layers = ['block5_conv2'] 

# best intermediate layers for style representation
style_layers = ['block1_conv1', 'block2_conv1', 'block3_conv1', 'block4_conv1', 'block5_conv1']

# get layers length
num_content_layers = len(content_layers)
num_style_layers = len(style_layers)

# set optimizer for style transfer
opt = tf.optimizers.Adam(learning_rate=0.02, beta_1=0.99, epsilon=1e-1)


def clip_0_1(image: tf.Tensor) -> tf.Tensor:
  """
  Function to keep the pixel values between 0 and 1

  Args:
      inputs (tf.Tensor): a tensor that represents an image

  Returns:
       tf.Tensor: a clipped tensor
  """
  return tf.clip_by_value(image, clip_value_min=0.0, clip_value_max=1.0)


def tensor_to_image(tensor: tf.Tensor) -> Image:
  """
  function to transform tensor to an image
  
  Args:
    tensor (tf.Tensor): tensor representing image

  Returns:
    PIL.Image: pillow image object
  """ 
  # multuply by 255 to undo normalization
  tensor = tensor*255
  # turn to array
  tensor = np.array(tensor, dtype=np.uint8)
  # remove the array dimension, leave only image
  if np.ndim(tensor)>3:
    assert tensor.shape[0] == 1
    tensor = tensor[0]
  # return array from image
  return Image.fromarray(tensor)


def load_img(path_to_img: str) -> tf.Tensor:
  """
  Function to load an image and limit its maximum dimension to 512 pixels
  
  Args:
    path_to_img (str): image path
    
  Returns:
    tf.Tensor: a tensor that represents an image
  """
  # set max dimensions
  max_dim = 512
  # read document
  img = tf.io.read_file(path_to_img)
  # decode to image
  img = tf.image.decode_image(img, channels=3)
  # convert to float, each val between [0,1]
  img = tf.image.convert_image_dtype(img, tf.float32)

  # get image width and hieght
  shape = tf.cast(tf.shape(img)[:-1], tf.float32)
  # get max height or width
  long_dim = max(shape)
  # get the ratio scale to 512
  scale = max_dim / long_dim

  # get the nex image shape by scale ratio
  new_shape = tf.cast(shape * scale, tf.int32)

  # rezise image
  img = tf.image.resize(img, new_shape)
  
  # expand dimension to image array
  img = img[tf.newaxis, :]
  return img


def vgg_layers(layer_names: List[str]) ->  tf.keras.Model:
  """ 
  Function to create a vgg model that returns a list of intermediate output values.

  Args:
    layer_names (List[str]): intermediate layers to output value
    
  Returns:
     tf.keras.Model:  a vgg model that returns a list of intermediate output values
  
  """
  # Build a VGG19 model loaded with pre-trained ImageNet weights
  vgg = tf.keras.applications.VGG19(include_top=False, weights='imagenet')
  
  # set model to not train itself
  vgg.trainable = False
  
  # get ouitput of intermediate layers
  outputs = [vgg.get_layer(name).output for name in layer_names]

  # create a vgg model
  model = tf.keras.Model([vgg.input], outputs)
  return model


def gram_matrix(input_tensor: tf.Tensor) -> tf.Tensor:
  """
  Function to calculate gram matrix of an image tensor (feature-wise outer product)

  Args:
    input_tensor (tf.Tensor): a tensor that represents an image

  Returns:
    tf.Tensor: the gram matrix result

  """
  # calculate the outer product of the feature vector with itself at each location
  result = tf.linalg.einsum('bijc,bijd->bcd', input_tensor, input_tensor)
  # get tensor shape
  input_shape = tf.shape(input_tensor)
  # calculate shape to avarge outer product
  num_locations = tf.cast(input_shape[1]*input_shape[2], tf.float32)
  # return averaging outer product over all locations
  return result/(num_locations)


class StyleContentModel(tf.keras.models.Model):
  """
  Model that returns the style and content tensors.
  """
  def __init__(self, style_layers, content_layers):
    #
    super(StyleContentModel, self).__init__()
    # get a vgg model that returns a list of intermediate output values.
    self.vgg =  vgg_layers(style_layers + content_layers)
    # set style layers
    self.style_layers = style_layers
    # set content layers
    self.content_layers = content_layers
    # set number of style layers
    self.num_style_layers = len(style_layers)
    # set model to be not trainable
    self.vgg.trainable = False


  def call(self, inputs) -> dict:
    """
    Overide the call method of object, to return the style and content tensors.

    Args:
        inputs (tf.Tensor): a tensor that represents an image, expects float input in [0,1]

    Returns:
       dict: the gram matrix result
    """
    # undo normalization of image
    inputs = inputs*255.0
    
    # pre process for vgg19 model
    preprocessed_input = tf.keras.applications.vgg19.preprocess_input(inputs)
    
    # foward pass image
    outputs = self.vgg(preprocessed_input)
    
    # get layers style and content output
    style_outputs, content_outputs = (outputs[:self.num_style_layers], outputs[self.num_style_layers:])

    # calc gram matrix for style output
    style_outputs = [gram_matrix(style_output) for style_output in style_outputs]

    # get content layers value as dict that key is the layer name
    content_dict = {content_name:value for content_name, value in zip(self.content_layers, content_outputs)}
    # get style layers value as dict that key is the layer name
    
    style_dict = {style_name:value for style_name, value in zip(self.style_layers, style_outputs)}
    # return the style and content tensors
    return {'content':content_dict, 'style':style_dict}





class DocumentStyleTransfer():
  """
  
  """

  def __init__(self, content_path, style_path):
    self.content_image = load_img(content_path)
    self.style_image = load_img(style_path)
    self.extractor =  StyleContentModel(style_layers, content_layers)
    self.style_targets = self.extractor(self.style_image)['style']
    self.content_targets = self.extractor(self.content_image)['content']
    self.image = tf.Variable(self.content_image)


  def style_content_loss(self, outputs: dict, style_weight: float, content_weight: float) -> float:
    """
    Function to calculate style and content loss
    
    Args:
        outputs (dict): style and content tensors

    Returns:
        float: style and content loss
    """
    # get style tensor
    style_outputs = outputs['style']
    
    # get content tensor
    content_outputs = outputs['content']
    
    # calc style loss
    style_loss = tf.add_n([tf.reduce_mean((style_outputs[name]-self.style_targets[name])**2) 
                          for name in style_outputs.keys()])
    
    # average loss by layers
    style_loss *= style_weight / num_style_layers

    # calculate content loss
    content_loss = tf.add_n([tf.reduce_mean((content_outputs[name]-self.content_targets[name])**2) 
                            for name in content_outputs.keys()])
    
    # average loss by layers
    content_loss *= content_weight / num_content_layers
    
    # add style and content loss
    loss = style_loss + content_loss
    return loss


  @tf.function()
  def train_step(self, image, style_weight: float, content_weight: float, total_variation_weight: float):
    # 
    with tf.GradientTape() as tape:
      # get image style and content tensors
      outputs = self.extractor(image)
      # calculate style and content loss
      loss = self.style_content_loss(outputs, style_weight, content_weight)
      # add total variation loss
      loss += total_variation_weight*tf.image.total_variation(image)

    # calc gradient descent
    grad = tape.gradient(loss, image)
    # apply gradient descent
    opt.apply_gradients([(grad, image)])
    # update image
    image.assign(clip_0_1(image))


  def render_image(self, results_dir:str = './', total_variation_weight:float = 1e-6, style_weight:float = 1e-6, content_weight:float = 2.5e-8, iter_save:int = 4000) -> None:
    """
    Method to render a style transfer image from content and style

    """
    # create directory for results
    if os.path.exists(results_dir):
        shutil.rmtree(results_dir)
    os.mkdir(results_dir)

    epochs = 10
    steps_per_epoch = 100

    step = 0
    for n in range(epochs):
      for m in range(steps_per_epoch):
        step += 1
        self.train_step(self.image, style_weight, content_weight, total_variation_weight)

    
    # set number of iteration of model
    iterations = 4000
    for i in range(1, iterations + 1):
      # apply a step in training process
      self.train_step(self.image, style_weight, content_weight, total_variation_weight)

      # for each iter_save iteration output results
      if i % iter_save == 0:
        file_name = f"{results_dir}/result_at_iteration_{i}.png"
        tensor_to_image(self.image).save(file_name) 