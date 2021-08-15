# importing the necessary modules
import requests
from bs4 import BeautifulSoup

# setting up constants for the program
LINK = "https://www.google.com/searchbyimage/upload"
FILE_LOCATION = r"Image location"

def reverse_image_search(img_location):
    """
        Reverse image searches the location of the image provided the argument.

            Parameters:
                img_location (string): The location to the image to searched.

            Returns:
                resulting_search (Beautiful Soup Object): The resulting
                    search for the image.
    """
    # the file data section
    file_data = {'encoded_image': (img_location, open(img_location, 'rb')), 'image_content': ''}
    # making a post request with the image
    response = requests.post(LINK, files = file_data, allow_redirects=False)
    # returning the new location of the search
    return response.headers['Location']

search_result = reverse_image_search(FILE_LOCATION)