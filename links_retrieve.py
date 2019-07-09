from lxml import html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib
import time
import random
import sys
import pickle

def page_load_status(driver):
	status = 'incomplete'
	while status == 'incomplete':
		print("Waiting...!")
		time.sleep(random.randint(2,3))
		status = driver.execute_script('return document.readyState;')
		if str(status) == 'complete':
			print("Page scrolling...!")
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	return ''

def get_links():
	driver = webdriver.Firefox()
	driver.get('https://pubpeer.com')

	time.sleep(20)
	page_load_status(driver)
	## flag to get information about
	## whether page is loaded
	downloaded = 0
	total = 2
	start = 1
	for k in range(1):
		if start == 1:
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(2)
			driver.find_element_by_css_selector(".btn-default").click()
			# auto scroll to down
			page_load_status(driver)
			start = start + 1
		else:
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(2)
			driver.find_element_by_css_selector(".btn-default[style='']").click()
			# auto scroll to down
			page_load_status(driver)
			start = start + 1

	list_links = driver.find_elements_by_css_selector('a')
	# print (len(list_links))

	list_links_new = []

	for i in range(len(list_links)):
		if i > 6 and i < 88: # Other Links are unncessary
			link = list_links[i].get_attribute("href")
			# print (link)
			list_links_new.append(link)

	# Checking if new links
	new_links = []
	with open("links", "rb") as fp:
	    old_links = pickle.load(fp)
	for link in list_links_new:
		if link not in old_links:
			new_links.append(link)

	# Dumping the new set of links obtained
	links_dump = open('links','wb')
	pickle.dump(list_links_new, links_dump)
	links_dump.close()
	print('Dumped Links')

	driver.close()

	return new_links

# new_links = get_links()
