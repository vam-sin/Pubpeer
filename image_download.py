from lxml import html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib
import time
import random
import sys
import pickle
driver = webdriver.Firefox()

with open("links", "rb") as fp:
    links = pickle.load(fp)

num_images = 0
for i in links:
    driver.get(i)
    time.sleep(5)
    # Image Download
    images = driver.find_elements_by_tag_name('img')
    for image in images:
    	src = image.get_attribute('src')
        if src!='https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif' and src!='https://pubpeer.com/img/verified.svg':
            print(image.get_attribute('src'))
            num_images = num_images + 1
    	    urllib.urlretrieve(src, "Images/download{}.jpeg".format(num_images))
            print 'downloaded an image'
