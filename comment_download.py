from lxml import html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib
import time
import random
import sys
import pickle
driver = webdriver.Firefox()

# Mysql setup
import mysql.connector
# User is root, with no password. Database name is db.
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="db"
)

mycursor = mydb.cursor()

def get_comments(links):
    # with open("links", "rb") as fp:
    #     links = pickle.load(fp)
    # with open("pairs", "rb") as fp:
    #     text_img_pairs = pickle.load(fp)
    # text_img_pairs = {}
    # Class is ibox-content markdown-body gallery, vertical-timeline-content ibox float-e-margins
    for i in links:
        driver.get(i)
        # time.sleep(5)
        # Comment Download
        comments = driver.find_elements_by_xpath("//div[@class='ibox-content markdown-body gallery']")
        # print(len(comments))
        for comment in comments:
            #print(i)
            #print(comment)
            text = comment.text
            #print(text)
            image = comment.find_elements_by_tag_name('img')
            #print(len(image))
            # if text not in text_img_pairs or image not in text_img_pairs[text]:
            # print("hi")
            # print(result)
            sql = "INSERT INTO  pairs VALUES (%s, %s, %s)"
            if(len(image)==0):
                text_img_pairs.update({text : "None"})
                check_sql = "select * from pairs where url='%s' and comment='%s' and image_link='%s'"%(i,text,image)
                mycursor.execute(sql)
                result = mycursor.fetchall()
                num_rows = mycursor.rowcount
                if num_rows==0:
                    val = (i, text, "None")
                    mycursor.execute(sql, val)
            else:
                for img in image:
                    image_link = img.get_attribute('src')
                    text_img_pairs.update({text : image_link})
                    check_sql = "select * from pairs where url='%s' and comment='%s' and image_link='%s'"%(i,text,image_link)
                    mycursor.execute(sql)
                    result = mycursor.fetchall()
                    num_rows = mycursor.rowcount
                    if num_rows==0:
                        val = (i, text, image_link)
                        mycursor.execute(sql, val)

    mydb.commit()
    print(text_img_pairs)

    pairs_dump = open('pairs','wb')
    pickle.dump(text_img_pairs, pairs_dump)
    pairs_dump.close()

    driver.close()
