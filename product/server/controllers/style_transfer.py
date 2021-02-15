import cv2
import base64
import numpy as np
from typing import List
from PIL import Image
from fastapi import APIRouter, UploadFile, File, Query
from machine_learning import style_transfer


# define default params for ml model
content_layer: List[str] = ['block4_conv2']
style_layers: List[str] = ['block1_conv1',
                          'block2_conv1',
                          'block3_conv1', 
                          'block4_conv1', 
                          'block5_conv1']
epochs_without_variation: int = 10
epochs_with_variation: int = 10
steps_per_epoch: int = 100
content_max_weight = 
style_max_weight = 
total_variation_max_weight = 


# create our router to end points
router: APIRouter = APIRouter()


@router.post("/renderImage/")
async def render_Image(content_loss:float = Query(..., gt=, le), style_loss: float, total_variation_loss: float, 
                     apply_dilation: bool, content_image: UploadFile = File(...),
                     style_image: UploadFile = File(...)) -> bytes:
    """
    End point to render style transfer image

    Args:
        content_loss (float): the content loss weight for ml model
        style_loss (float): the style loss weight for ml model
        total_variation_loss (float): the total variation loss weight for ml model
        apply_dilation (bool): boolean to apply dilation on content image or not
        content_image (UploadFile, optional): content image
        style_image (UploadFile, optional): style image

    Returns:
        bytes: the rendered image
    """

    # test files are image
    if content_image.content_type not in ["image/png", "image/jpg", "image/jpeg"]:
        pass

    
    if style_image.content_type not in ["image/png", "image/jpg", "image/jpeg"]:
        pass

    # validate parameters


    # read content image to numpy array
    content_img: bytes = await content_image.read()
    content_img: np.ndarray = np.fromstring(content_img, np.uint8)
    content_img: np.ndarray = cv2.imdecode(content_img, cv2.IMREAD_COLOR)
    content_img: np.ndarray = cv2.cvtColor(content_img, cv2.COLOR_BGR2RGB)

    # read style image to numpy array
    style_img: bytes = await style_image.read()
    style_img: np.ndarray = np.fromstring(style_img, np.uint8)
    style_img: np.ndarray = cv2.imdecode(style_img, cv2.IMREAD_COLOR)
    style_img: np.ndarray = cv2.cvtColor(style_img, cv2.COLOR_BGR2RGB)

    # apply dilation on content image
    if apply_dilation:
        kernel: np.ndarray = np.ones((5,5), np.uint8)
        content_img = cv2.erode(content_img, kernel, iterations = 1)

    """
    # apply ml model
    result: Image = style_transfer.render_image(content_img, style_img, content_layer, style_layers, 
                                style_loss, content_loss, total_variation_loss, 
                                epochs_without_variation, epochs_with_variation, steps_per_epoch)
    result.save('test.png')
    # convert Image to np array
    result: np.ndarray = np.asarray(result)
    # convert to BGR for imencode
    result = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
    # encode result and return it
    _, encoded_img = cv2.imencode('.PNG', np.asarray(result))
    encoded_img: bytes = base64.b64encode(encoded_img)
    """
    # temp  
    _, encoded_img = cv2.imencode('.PNG', style_img)
    encoded_img: bytes = base64.b64encode(encoded_img)
    return encoded_img
