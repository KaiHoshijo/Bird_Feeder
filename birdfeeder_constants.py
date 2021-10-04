# importing the required modules
import os
from datetime import datetime
# creating the constants
LINK = "https://www.google.com/searchbyimage/upload"
GECKO_PATH = os.getcwd() + r"/geckodriver/geckodriver.exe"
FILE_LOCATION = os.getcwd() + r"/bird_images/fuwd-2.jpg"
DIRECTORY_LOCATION = os.getcwd() + r"/bird_images/"
BIRD_LOCATION = "bird_images_locations.txt"
SERVER_NAME = "smtp.gmail.com"
SERVER_PORT = 465
SENDER_ADDRESS = "to@email.com"
SENDER_PASSWORD = "PASSWORD"
RECEIVER_ADDRESS = "from@email.com"
SUBJECT = "Bird Photos Of " + str(datetime.now().date())