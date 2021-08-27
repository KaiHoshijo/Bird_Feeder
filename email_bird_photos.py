# importing the required modules
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import imghdr

import birdfeeder_constants as bfc

def send_email():
    """
        This will send the bird images and links to similar birds
        at 8:00 PM every day. 

            Parameters:
                None
            
            Returns:
                None
    """
    # creating an empty email message
    message = EmailMessage()
    # send the to address, from address, and subject of the email
    message["To"] = bfc.SENDER_ADDRESS
    message["From"] = bfc.RECEIVER_ADDRESS
    message["Subject"] = bfc.SUBJECT
    multipart_body = MIMEMultipart()

    with smtplib.SMTP_SSL(bfc.SERVER_NAME, bfc.SERVER_PORT) as emailer:
        # logging into the email service
        emailer.login(bfc.SENDER_ADDRESS, bfc.SENDER_PASSWORD)
        # creating the body of the message
        body = "\n\nHello,\n\nHere are the birds that visited today:\n\n"
        # getting bird images and webpage links from the bird location file
        with open(bfc.BIRD_LOCATION, "r") as bird_file:
            # getting the webpage links and image file locations
            # every other line is a bird image file
            # the other is one filled with webpage links
            for img_index, line in enumerate(bird_file.readlines()):
                if img_index % 2 == 0:
                    current_img = line.strip()
                    # getting the image's data and type
                    with open(current_img, "rb") as current_img_file:
                        img_data = current_img_file.read()
                        img_type = imghdr.what(current_img)
                    # adding the image as an attachment to the current message
                    message.add_attachment(img_data, maintype='image',
                        subtype=img_type, filename=f"bird_image_{img_index+1}")
                else:
                    webpage_links = line.strip().split(",")
                    # creating the content of the message
                    body += f"\tFor bird image {img_index + 1}, " + \
                        "these are similar images:\n"
                    for webpage_link in webpage_links:
                        body += f"\t\t{webpage_link}\n"
        # ending the message
        body += """\nThanks for looking at the birds!\
                    \nWill return with more tomorrow!\
                    \n\nYours truly,\n Kai"""
        multipart_body.attach(MIMEText(body))
        message.attach(multipart_body)
        # sending the email to the receiver address
        emailer.send_message(message)
        # once the email is sent, clear the bird_images_location.txt file
        # don't want to send a repeated message
        with open(bfc.BIRD_LOCATION, "w") as clear_file:
            pass
send_email()