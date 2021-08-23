# importing the required modules
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import imghdr

import birdfeeder_constants as bfc

def get_image_data(img_location):
    """
        This returns the name, binary, and image type of the image file.
        
            Parameters:
                img_location (string): The file location of the image file.
            
            Returns:
                img_name (string): The name of the image.
                img_binary (binary): The binary of the image.
                img_type (string): The type of the image.
    """
    img_name = ""
    img_binary = None
    img_type = ""
    with open(img_location, "rb") as img:
        img_name = img.name
        img_binary = img.read()
        img_type = imghdr.what(img_name)
    return img_name, img_binary, img_type

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
        # the containers for both the image files and webpage links
        img_files = []
        webpage_links = []
        body = "\n\nHello,\nHere are the birds that visited today:\n\n"
        # getting bird images and webpage links from the bird location file
        with open(bfc.BIRD_LOCATION, "r") as bird_file:
            # every other line is a bird image file
            # the other is one filled with webpage links
            index = 0
            for line in bird_file.readlines():
                if index % 2 == 0:
                    img_files.append(line.strip())
                else:
                    webpage_links.append(line.strip().split(","))
                index += 1
        # adding each attachment to the file
        for img_index, img_file in enumerate(img_files):
            # getting the image's name, data, and type
            img_name, img_binary, img_type = get_image_data(img_file)
            # adding the image as an attachment to the current message
            message.add_attachment(img_binary, 
                        maintype='image', subtype=img_type,
                        filename=f"bird_image_{img_index+1}")
            # creating the content of the message
            body += f"\tFor the bird {img_index + 1}, these links are provided:\n"
            for webpage_link in webpage_links[img_index]:
                body += f"\t\t{webpage_link}\n"
        # ending the message
        body += """\nThanks for looking at the birds!\
                    \nWill return with more tomorrow!\
                    \n\nYours truly,\n Kai"""
        multipart_body.attach(MIMEText(body))
        message.attach(multipart_body)
        # sending the email to the receiver address
        emailer.send_message(message)
send_email()