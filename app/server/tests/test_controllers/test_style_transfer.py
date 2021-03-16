"""
Tests for style transfer controller
"""


import os
import numpy as np
from typing import Dict
from fastapi.testclient import TestClient
from server.controllers.main import app
from unittest import mock
from unittest.mock import patch
from requests import Response


# get dir path
dir_path: str = os.path.dirname(os.path.realpath(__file__))

# create a client for testing
client = TestClient(app)


@patch('server.controllers.style_transfer.render_image_background')
def test_render_image_without_images(
    mock_render_image_background: mock.MagicMock) -> None:
    """
    Test method of style transfer controller api end point with images

    Args:
        mock_render_image_background (mock.MagicMock): mock
    """

    # Arrange
    data: Dict[str, str] = {"email": "test@test.com",
            "content_loss": "150",
            "style_loss": "0.01",
            "total_variation_loss": "30",
            "apply_dilation": "true"}

    # Act
    response: Response = client.post("/api/styleTransfer/renderImage/",
                                     data=data)

    # Assert
    mock_render_image_background.assert_called()
    assert mock_render_image_background.call_args[0][:4] == ('test@test.com',
                                                             150.0, 0.01, 30.0)
    assert response.status_code == 200


@patch('server.controllers.style_transfer.render_image_background')
def test_render_image_with_images(
    mock_render_image_background: mock.MagicMock) -> None:
    """
    Test method of style transfer controller api end point without images

    Args:
        mock_render_image_background (mock.MagicMock): mock
    """

    # Arrange
    files: Dict[str, tuple] = {
            "content_image": ("test_content_image",
                               open(dir_path + '/../../data/modern.png', "rb"),
                               "image/png"),
            "style_image": ("test_style_image",
                             open(dir_path + '/../../data/historical.png', "rb"),
                             "image/png")}

    data: Dict[str, str] = {"email": "test@test.com",
            "content_loss": "150",
            "style_loss": "0.01",
            "total_variation_loss": "30",
            "apply_dilation": "true"}

    # Act
    response: Response = client.post("/api/styleTransfer/renderImage/",
                                     data=data, files=files)

    # Assert
    assert mock_render_image_background.call_args[0][:4] == ('test@test.com',
                                                             150.0, 0.01, 30.0)
    assert response.status_code == 200


@patch('server.controllers.style_transfer.render_image_background')
def test_render_image_with_wrong_images(
    mock_render_image_background: mock.MagicMock) -> None:
    """
    Test method of style transfer controller api end point with wrong images

    Args:
        mock_render_image_background (mock.MagicMock): mock
    """
    # Arrange
    files: Dict[str, tuple] = {"content_image": ("test_content_image",
                               np.full((3, 3, 3), 255).tobytes(),
                               "image/png"),
             "style_image": ("test_style_image",
                             np.full((3, 3, 3), 255).tobytes(),
                             "image/png")}

    data: Dict[str, str] = {"email": "test@test.com",
            "content_loss": "150",
            "style_loss": "0.01",
            "total_variation_loss": "30",
            "apply_dilation": "true"}

    # Act
    response: Response = client.post("/api/styleTransfer/renderImage/",
                                     data=data, files=files)

    # Assert
    mock_render_image_background.assert_not_called()
    assert response.status_code == 422
    assert response.json()['detail'] == ('Unable to process image file')


@patch('server.controllers.style_transfer.render_image_background')
def test_render_image_wrong_max_content_loss(
    mock_render_image_background: mock.MagicMock) -> None:
    """
    Test method of style transfer controller api end point with content
    loss larger than allowed

    Args:
        mock_render_image_background (mock.MagicMock): mock
    """
    # Arrange
    data: Dict[str, str] = {"email": "test@test.com",
            "content_loss": "1000000.0",
            "style_loss": "0.01",
            "total_variation_loss": "30",
            "apply_dilation": "true"}

    # Act
    response: Response = client.post("/api/styleTransfer/renderImage/",
                                     data=data)

    # Assert
    mock_render_image_background.assert_not_called()
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == ('ensure this value is'
                                                   ' less than or equal to'
                                                   ' 100000.0')


@patch('server.controllers.style_transfer.render_image_background')
def test_render_image_wrong_min_content_loss(
    mock_render_image_background: mock.MagicMock) -> None:
    """
    Test method of style transfer controller api end point with content
    loss smaller than allowed

    Args:
        mock_render_image_background (mock.MagicMock): mock
    """
    # Arrange
    data: Dict[str, str] = {"email": "test@test.com",
            "content_loss": "-1",
            "style_loss": "0.01",
            "total_variation_loss": "30",
            "apply_dilation": "true"}

    # Act
    response: Response = client.post("/api/styleTransfer/renderImage/",
                                     data=data)

    # Assert
    mock_render_image_background.assert_not_called()
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == ('ensure this value is'
                                                   ' greater than or equal to'
                                                   ' 10.0')


@patch('server.controllers.style_transfer.render_image_background')
def test_render_image_wrong_max_style_loss(
    mock_render_image_background: mock.MagicMock) -> None:
    """
    Test method of style transfer controller api end point with style
    loss larger than allowed

    Args:
        mock_render_image_background (mock.MagicMock): mock
    """
    # Arrange
    data: Dict[str, str] = {"email": "test@test.com",
            "content_loss": "150",
            "style_loss": "0.02",
            "total_variation_loss": "30",
            "apply_dilation": "true"}

    # Act
    response: Response = client.post("/api/styleTransfer/renderImage/",
                                     data=data)

    # Assert
    mock_render_image_background.assert_not_called()
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == ('ensure this value is'
                                                   ' less than or equal to'
                                                   ' 0.01')


@patch('server.controllers.style_transfer.render_image_background')
def test_render_image_wrong_min_style_loss(
    mock_render_image_background: mock.MagicMock) -> None:
    """
    Test method of style transfer controller api end point with style
    loss smaller than allowed

    Args:
        mock_render_image_background (mock.MagicMock): mock
    """
    # Arrange
    data: Dict[str, str] = {"email": "test@test.com",
            "content_loss": "150",
            "style_loss": "0.00",
            "total_variation_loss": "30",
            "apply_dilation": "true"}

    # Act
    response: Response = client.post("/api/styleTransfer/renderImage/",
                                     data=data)

    # Assert
    mock_render_image_background.assert_not_called()
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == ('ensure this value is'
                                                   ' greater than or equal to'
                                                   ' 0.01')


@patch('server.controllers.style_transfer.render_image_background')
def test_render_image_wrong_max_total_variation_loss(
    mock_render_image_background: mock.MagicMock) -> None:
    """
    Test method of style transfer controller api end point with total
    variation loss larger than allowed

    Args:
        mock_render_image_background (mock.MagicMock): mock
    """

    # Arrange
    data: Dict[str, str] = {"email": "test@test.com",
            "content_loss": "150",
            "style_loss": "0.01",
            "total_variation_loss": "50",
            "apply_dilation": "true"}

    # Act
    response: Response = client.post("/api/styleTransfer/renderImage/",
                                     data=data)

    # Assert
    mock_render_image_background.assert_not_called()
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == ('ensure this value is'
                                                   ' less than or equal to'
                                                   ' 30.0')


@patch('server.controllers.style_transfer.render_image_background')
def test_render_image_wrong_min_total_variation_loss(
    mock_render_image_background: mock.MagicMock) -> None:
    """
    Test method of style transfer controller api end point with total
    variation loss smaller than allowed

    Args:
        mock_render_image_background (mock.MagicMock): mock
    """
    # Arrange
    data: Dict[str, str] = {"email": "test@test.com",
            "content_loss": "150",
            "style_loss": "0.01",
            "total_variation_loss": "20",
            "apply_dilation": "true"}

    # Act
    response: Response = client.post("/api/styleTransfer/renderImage/",
                                     data=data)

    # Assert
    mock_render_image_background.assert_not_called()
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == ('ensure this value is'
                                                   ' greater than or equal to'
                                                   ' 30.0')


@patch('server.services.mail_service.send_image_by_email')
@patch('server.machine_learning.style_transfer.render_image')
def test_render_render_image_background(
    mock_render_image: mock.MagicMock,
    mock_send_image_by_email: mock.MagicMock) -> None:
    """
    Test method of style transfer controller to test render image background
    method

    Args:
        mock_render_image_background (mock.MagicMock): mock
    """
    # Arrange
    data: Dict[str, str] = {"email": "test@test.com",
            "content_loss": "150",
            "style_loss": "0.01",
            "total_variation_loss": "30",
            "apply_dilation": "true"}

    # Act
    response: Response = client.post("/api/styleTransfer/renderImage/",
                                     data=data)

    # Assert
    mock_render_image.assert_called()
    mock_send_image_by_email.assert_called()
    assert response.status_code == 200
