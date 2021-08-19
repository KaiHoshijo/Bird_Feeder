# importing the necessary modules
import requests
from selenium import webdriver
import os

# setting up constants for the program
LINK = "https://www.google.com/searchbyimage/upload"
FILE_LOCATION = os.getcwd() + r"/bird_images/fuwd-2.jpg"
GECKO_PATH = os.getcwd() + r"/geckodriver/geckodriver.exe"

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
print(search_result)

def search_related_images_for_name(search_result, amount_of_pages=5):
    """
        Utilizes the previous reverse image search to find similar images
        for the name of the bird provided in the image.

            Parameters:
                search_result (string): This is the string of the link to
                google's reverse image search.
                amount_of_pages (int): This is the amount of webpages returned
                back to the user.
            
            Returns:
                data_page (string list): A list of the top 5 websites related
                to the reverse image search.
    """
    # starting the driver for selenium
    driver = webdriver.Firefox(executable_path=GECKO_PATH)
    # connecting the driver to the search result
    driver.get(search_result)
    
    # getting the iur div
    iur_div = driver.find_element_by_id("iur")
    # getting the images universal data-attrid tag because this is all the 
    # similar images to the one provided in the google search
    images_universal_xpath = "//div[@data-attrid='images universal']"
    images_universal_elements = iur_div.find_elements_by_xpath(images_universal_xpath)
    print(len(images_universal_elements))

    # getting the data-lpage attribute for each iur element
    # appending that attribute to a data_page
    data_page = []
    for element in images_universal_elements[:amount_of_pages]:
        data_page.append(element.get_attribute("data-lpage"))

    # closing the firefox driver
    driver.close()

    # returning the data_page
    return data_page

search_related_images_for_name(search_result)