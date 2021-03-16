"""
Tests for mail service
"""


from PIL import Image
from unittest import mock
from server.services import mail_service
from unittest.mock import patch


@patch('smtplib.SMTP')
def test_send_image_by_email_smtp_constructor(
    mock_smtp: mock.MagicMock) -> None:
    """
    Test method of mail service

    Args:
        mock_smtp (mock.MagicMock): mock
    """
    # Arrange
    img: Image = Image.new('RGB', (60, 30), color = 'red')
    text: str = 'test'
    email: str = 'test@test.com'

    # Act
    mail_service.send_image_by_email(img, text, email)

    # Assert
    assert mock_smtp.call_args == (('smtp.gmail.com', 587),)


@patch('smtplib.SMTP', autospec=True)
def test_send_image_by_email_called_starttls(
    mock_smtp: mock.MagicMock) -> None:
    """
    Test method of mail service

    Args:
        mock_smtp (mock.MagicMock): mock
    """
    # Arrange
    img: Image = Image.new('RGB', (60, 30), color = 'red')
    text: str = 'test'
    email: str = 'test@test.com'

    # Act
    mail_service.send_image_by_email(img, text, email)

    # Assert
    print(mock_smtp.method_calls)
    name, args, kwargs = mock_smtp.method_calls.pop(0)
    assert name == '().starttls'
    assert args == ()
    assert kwargs == {}


@patch('smtplib.SMTP', autospec=True)
def test_send_image_by_email_called_login(
    mock_smtp: mock.MagicMock) -> None:
    """
    Test method of mail service

    Args:
        mock_smtp (mock.MagicMock): mock
    """
    # Arrange
    img: Image = Image.new('RGB', (60, 30), color = 'red')
    text: str = 'test'
    email: str = 'test@test.com'

    # Act
    mail_service.send_image_by_email(img, text, email)

    # Assert
    name, args, kwargs = mock_smtp.method_calls.pop(1)
    assert name == '().login'
    assert args == ('hstyle.service@gmail.com', 'HStyle1234')
    assert kwargs == {}


@patch('smtplib.SMTP', autospec=True)
def test_send_image_by_email_called_sendmail(
    mock_smtp: mock.MagicMock) -> None:
    """
    Test method of mail service

    Args:
        mock_smtp (mock.MagicMock): mock
    """
    # Arrange
    img: Image = Image.new('RGB', (60, 30), color = 'red')
    text: str = 'test'
    email: str = 'test@test.com'

    # Act
    mail_service.send_image_by_email(img, text, email)

    # Assert
    name, args, kwargs = mock_smtp.method_calls.pop(2)
    assert name == '().sendmail'
    assert args[0] == 'HStyle Service'
    assert args[1] == 'test@test.com'
    assert kwargs == {}


@patch('smtplib.SMTP', autospec=True)
def test_send_image_by_email_called_quit(
    mock_smtp: mock.MagicMock) -> None:
    """
    Test method of mail service

    Args:
        mock_smtp (mock.MagicMock): mock
    """
    # Arrange
    img: Image = Image.new('RGB', (60, 30), color = 'red')
    text: str = 'test'
    email: str = 'test@test.com'

    # Act
    mail_service.send_image_by_email(img, text, email)

    # Assert
    name, args, kwargs = mock_smtp.method_calls.pop(3)
    assert name == '().quit'
    assert args == ()
    assert kwargs == {}

@patch('smtplib.SMTP', autospec=True)
@patch('email.mime.multipart.MIMEMultipart', autospec=True)
def test_send_image_by_email_mimemultipart_constructor(
    mock_mimemultipart: mock.MagicMock, _) -> None:
    """
    Test method of mail service

    Args:
        mock_mimemultipart (mock.MagicMock): mock
    """
    # Arrange
    img: Image = Image.new('RGB', (60, 30), color = 'red')
    text: str = 'test'
    email: str = 'test@test.com'

    # Act
    mail_service.send_image_by_email(img, text, email)

    # Assert
    assert mock_mimemultipart.call_args is None

@patch('smtplib.SMTP', autospec=True)
@patch('email.mime.image.MIMEImage', autospec=True)
def test_send_image_by_email_mimeimage_constructor(
    mock_mimeimage: mock.MagicMock, _) -> None:
    """
    Test method of mail service

    Args:
        mock_mimeimage (mock.MagicMock): mock
    """
    # Arrange
    img: Image = Image.new('RGB', (60, 30), color = 'red')
    text: str = 'test'
    email: str = 'test@test.com'

    # Act
    mail_service.send_image_by_email(img, text, email)

    # Assert
    assert mock_mimeimage.call_args is None


@patch('smtplib.SMTP', autospec=True)
@patch('email.mime.text.MIMEText', autospec=True)
def test_send_image_by_email_mimetext_constructor(
    mock_mimetext: mock.MagicMock, _) -> None:
    """
    Test method of mail service

    Args:
        mock_mimetext (mock.MagicMock): mock
    """
    # Arrange
    img: Image = Image.new('RGB', (60, 30), color = 'red')
    text: str = 'test'
    email: str = 'test@test.com'

    # Act
    mail_service.send_image_by_email(img, text, email)

    # Assert
    assert mock_mimetext.call_args is None
