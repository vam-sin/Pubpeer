# Every Image and its respective following text will be put into files
# referencing each other.
# The data of the links will taken from the links pickle file
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.request import urlretrieve
from urllib.error import HTTPError, URLError
from selenium.common.exceptions import StaleElementReferenceException
import time
import random
import sys
import pickle
driver = webdriver.Firefox()

def folder_generate():
    with open("links", "rb") as fp:
        links = pickle.load(fp)
    for i in links:
        time.sleep(3)
        driver.get(i)
        start = 1
        # time.sleep(5)
        # Comment Download
        comments = driver.find_elements_by_xpath("//div[@class='ibox-content markdown-body gallery']")
        # print(len(comments))
        for comment in comments:
            #print(i)
            #print(comment)
            try:
                text = comment.text
            except StaleElementReferenceException as err:
                print(err)
            #print(text)
            x = str(i)
            x = x.replace('/','_')
            x = x.replace('https:__pubpeer.com_publications', 'pubpeer')
            try:
                image = comment.find_elements_by_tag_name('img')
            except StaleElementReferenceException as err:
                print(err)
            f = open("Comments/" + str(x) + "_" + str(start) + ".txt", "a")
            if(len(image)==0):
                f.write(text)
                f.write("\n")
            else:
                for img in image:
                    try:
                        image_link = img.get_attribute('src')
                    except StaleElementReferenceException as err:
                        print(err)
                    start = start + 1
                    try:
                        urlretrieve(image_link, "Images/" + str(x) + "_" + str(start) + ".jpeg")
                    except HTTPError as err:
                        print(err)
                    except StaleElementReferenceException as err:
                        print(err)
                    except URLError as err:
                        print(err)




    driver.close()

folder_generate()
