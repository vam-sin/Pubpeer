from lxml import html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time
import random
import sys
import pickle
driver = webdriver.Firefox()
driver.get('https://pubpeer.com')

# click on "Load more" button
# page content
def getPageContent(driver):
	page_source = driver.page_source
	page_content = html.document_fromstring(page_source)
	page_child = page_content.getchildren()[1].getchildren()[3].getchildren()[0].getchildren()[2]
	page_child = page_child.getchildren()[0].getchildren()[0].getchildren()[1]
	pub_stats = page_child.getchildren()[1].getchildren()[0].getchildren()[0]
	pub_list = page_child.getchildren()[1].getchildren()[0].getchildren()[1].getchildren()[0].getchildren()
	number_pubs = int(pub_stats.getchildren()[0].text.split("(")[1].split(')')[0])
	current_status = {'total': number_pubs,'downloaded': len(pub_list), 'pubs': pub_list}
	return current_status

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

time.sleep(20)
page_load_status(driver)
## flag to get information about
## whether page is loaded
downloaded = 0
total = 10
start = 1
while total > downloaded:
	if start == 1:
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(2)
		#  driver.findElement(By.xpath("//button[text()='Load more']")).click();
		driver.find_element_by_css_selector(".btn-default").click()
		# auto scroll to down
		page_load_status(driver)
		cur_content = getPageContent(driver)
		total = cur_content['total']
		downloaded = cur_content['downloaded']
		print("@@@@@@@@@@@@@@@@@@@")
		print("downloaded " + str(downloaded))
		print("# run " + str(start))
		print("@@@@@@@@@@@@@@@@@@@")
		start = start + 1
	else:
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(2)
		driver.find_element_by_css_selector(".btn-default[style='']").click()
		# auto scroll to down
		page_load_status(driver)
		cur_content = getPageContent(driver)
		total = cur_content['total']
		downloaded = cur_content['downloaded']
		print("@@@@@@@@@@@@@@@@@@@")
		print("downloaded " + str(downloaded))
		print("# run " + str(start))
		print("@@@@@@@@@@@@@@@@@@@")
		start = start + 1


# https://pubpeer.com/api/search/?q=27695031
def extract_info(xx):
	if len(xx.getchildren()[0].getchildren()) > 0:
		info = xx.getchildren()[0].getchildren()[0].getchildren()[1].getchildren()[0].getchildren()[0].getchildren()[0]
		pub_title = info.text
		pub_pubpeer_hashkey = info.items()[0][1]
		out = {'title':pub_title, 'hashkey':pub_pubpeer_hashkey.split('/')[2]}
	else:
		out = {'title':'', 'hashkey':''}
	return out

i = 0
pp_hashkeys = []
for pub in cur_content['pubs']:
	out = extract_info(pub)
	if len(out['hashkey']) > 0:
		pp_hashkeys.append(out['hashkey'])
	print i, '. ',out['hashkey']
	i = i + 1
pickle_obs = open('./pubpeer-10K-hashkeys.pickle','wb')
pickle.dump(pp_hashkeys, pickle_obs)
pickle_obs.close()
