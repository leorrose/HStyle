"""
Email service responsable for all email services through the application.
"""


import smtplib
import io
from pydantic import EmailStr
from PIL import Image
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


def send_image_by_email(img: Image, email_text: str, email: EmailStr
                        ) -> None:
    """
    Method to send image with text by email

    Args:
        img (Image): the image to send
        email_text (str): the text to send
        email (EmailStr): receiver email address
    """
    # sertup email client
    server: smtplib.SMTP = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('hstyle.service@gmail.com', 'HStyle1234')

    # Create the container (outer) email message.
    msg: MIMEMultipart = MIMEMultipart()
    msg['Subject'] = 'Historical Style Generator'
    msg['To'] = email
    msg['From'] = 'HStyle Service'

    # convert Image to np array
    img_data: io.BytesIO = io.BytesIO()
    img.save(img_data, format='PNG')
    img_data: bytes = img_data.getvalue()

    # attach image to email
    img: MIMEImage = MIMEImage(img_data, _subtype='.PNG', name='render.png')
    msg.attach(img)

    # attach text to email
    body: MIMEText = MIMEText(email_text)
    msg.attach(body)

    # Send the email and close server
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()
