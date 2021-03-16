"""
Style transfer api controller for HStyle api. responsable for the style
transfer end point and applying the style transfer.
"""


import os
import cv2
import numpy as np
from server.machine_learning import style_transfer
from server.services import mail_service
from typing import List
from pydantic import EmailStr
from fastapi import (APIRouter, UploadFile, File, Body, HTTPException,
                     status, BackgroundTasks)
from starlette.responses import Response
from PIL import Image


# get dir path
dir_path: str = os.path.dirname(os.path.realpath(__file__))

# content layer for style transfer model
content_layer: List[str] = ['block4_conv2']

# style layers for style transfer model
style_layers: List[str] = ['block1_conv1', 'block2_conv1',
                           'block3_conv1', 'block4_conv1',
                           'block5_conv1']

# amount of epochs to apply withot total variation
epochs_without_variation: int = 10

# amount of epochs to apply with total variation
epochs_with_variation: int = 10

# amount of steps per each epoch
steps_per_epoch: int = 100

# content loss
content_max_weight: float = 100000.0
content_min_weight: float = 10.0

# style loss
style_max_weight: float = 0.01
style_min_weight: float = 0.01

# total variation loss
total_variation_max_weight: float = 30.0
total_variation_min_weight: float = 30.0

# deafult content image
content_img_deafult: np.ndarray = np.asarray(
    Image.open(dir_path + '/../data/modern.png'))
# deafult style image
style_img_deafult: np.ndarray = np.asarray(
    Image.open(dir_path + '/../data/historical.png'))

# create our router to style transfer api
router: APIRouter = APIRouter()


async def read_image_from_api(api_img: UploadFile) -> np.ndarray:
    """
    Method to read an UploadFile from api as image

    Args:
        api_img (UploadFile): an image file

    Raises:
        HTTPException: if image is not readable

    Returns:
        np.ndarray: RGB image as numpy array
    """
    try:
        # read image as bytes/chars
        img: bytes = await api_img.read()
        # create numpy array from bytes
        img: np.ndarray = np.frombuffer(img, np.uint8)
        # create image from bytes
        img: np.ndarray = cv2.imdecode(img, cv2.IMREAD_COLOR)
        # transform BGR to RGB
        img: np.ndarray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Unable to process image file"
        ) from err


def render_image_background(email: EmailStr, content_loss: float, style_loss: float,
                 total_variation_loss: float, content_img: np.ndarray,
                 style_img: np.ndarray) -> None:
    """
    background method to apply style transfer and send by email

    Args:
        email (EmailStr): receiver email
        content_loss (float): the content loss weight for style transfer model
        style_loss (float): the style loss weight for style transfer model
        total_variation_loss (float): the total variation loss weight for
        content_img (np.ndarray): content image
        style_img (np.ndarray): style image
    """
    # apply style transfer model
    result: Image = style_transfer.render_image(content_img, style_img,
                                                content_layer, style_layers,
                                                style_loss, content_loss,
                                                total_variation_loss,
                                                epochs_without_variation,
                                                epochs_with_variation,
                                                steps_per_epoch)
    # send image by email
    msg = ('Thanks for using HStyle!\nwe added the Rendered Image'
           ', We hope u are satisfied from our service')
    mail_service.send_image_by_email(result, msg, email)


@router.post("/renderImage/")
async def render_image(background_tasks: BackgroundTasks,
                 email: EmailStr = Body(...),
                 content_loss: float = Body(..., ge=content_min_weight,
                                             le=content_max_weight),
                 style_loss: float = Body(..., ge=style_min_weight,
                                           le=style_max_weight),
                 total_variation_loss: float = Body(
                     ..., ge=total_variation_min_weight,
                     le=total_variation_max_weight),
                 apply_dilation: bool = Body(...),
                 content_image: UploadFile = File(None),
                 style_image: UploadFile = File(None)) -> Response:
    """
    End point for using the style transfer model in order to render a content
    image with the style of style image.
    \f
    Args:
        email(EmailStr): email to send to user
        content_loss (float): the content loss weight for style transfer model
        style_loss (float): the style loss weight for style transfer model
        total_variation_loss (float): the total variation loss weight for
        style transfer model
        apply_dilation (bool): boolean to apply dilation on content image
        content_image (UploadFile, optional): content image
        style_image (UploadFile, optional): style image

    Returns:
        Response: status OK.
    """

    # test content image was provided and its type
    if content_image is not None:
        content_img: np.ndarray = await read_image_from_api(content_image)
    # apply deafault content image
    else:
        content_img: np.ndarray = content_img_deafult.copy()

    # test style image was provided and its type
    if style_image is not None:
        style_img: np.ndarray = await read_image_from_api(style_image)
    # apply deafault style image
    else:
        style_img: np.ndarray = style_img_deafult.copy()

    # apply dilation on content image
    if apply_dilation:
        kernel: np.ndarray = np.ones((5, 5), np.uint8)
        content_img: np.ndarray = cv2.erode(content_img, kernel, iterations=1)

    # run model + email send in background
    background_tasks.add_task(render_image_background, email, content_loss,
                              style_loss, total_variation_loss,
                              content_img, style_img)

    return Response(status_code=status.HTTP_200_OK)
