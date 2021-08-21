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

    # getting the data-lpage attribute for each iur element
    # appending that attribute to a data_page
    data_page = []
    for element in images_universal_elements[:amount_of_pages]:
        data_page.append(element.get_attribute("data-lpage"))

    # closing the firefox driver
    driver.close()

    # returning the data_page
    return data_page 

def create_email_file(img_location, data_pages):
    """
        This creates the file "bird_images_location.txt"
        or it appends to it if it already exists. Additionally,
        this function adds the img_location on one line then
        all the data_pages are on the same line separated by a comma.

        Parameters:
            img_location (string): The string location to the image.
            data_pages (list of strings): The links of similar images to the
            one provided.
        
        Returns:
            None
    """
    # Creating the file or appending to it if it already exists.
    with open("bird_images_locations.txt", "a") as bird_file:
        # the file will be formated as follows:
        # img_location
        # data_page,data_page,data_page,...
        # and so on
        bird_file.write(img_location)
        # creating each comma separated data page
        comma_separated_data_pages = "\n"
        for i in range(len(data_pages)-1):
            data_page = data_pages[i]
            comma_separated_data_pages += data_page + ','
        comma_separated_data_pages += data_pages[-1]
        bird_file.write(comma_separated_data_pages + "\n")
search_result = reverse_image_search(FILE_LOCATION)
data_pages = search_related_images_for_name(search_result)
create_email_file(FILE_LOCATION, data_pages)