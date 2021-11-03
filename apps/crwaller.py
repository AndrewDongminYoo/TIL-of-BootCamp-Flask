import time

from pymongo import MongoClient
import re
import mongoengine as me
from pymongo.collection import Collection
from selenium import webdriver
from urllib import parse
import requests
from bs4 import BeautifulSoup
import csv
from pprint import pprint
import os

from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
os.popen("mongod")
client = MongoClient()
db = client.get_database("dbmember")
students: Collection = db.get_collection("student")


def tistory_blog():
    members = students.find({"blog_type": "tistory"}, {"_id": False})
    tistory_urls = []
    for member in members:
        if member["blog"].strip():
            tistory_urls.append((member['username'], member['blog'], member["blog_type"]))
    for name, url, types in tistory_urls:
        target_part = parse.urlparse(url+"sitemap")
        target = parse.urlunparse(target_part)
        res = requests.get(target)
        soup = BeautifulSoup(res.text, 'html.parser')
        regex = re.compile(url+r"\d+")
        url_list = sorted(regex.findall(soup.text))
        if not url_list:
            regex = re.compile(url+"entry/" + r"[\-%\w\d]+")
            url_list = sorted(regex.findall(soup.text))
        students.update_one({"username": name}, {"$set": {"blog_list": url_list}}, upsert=True)


def velog_blog():
    velog_mem = students.find({"blog_type": "velog"}, {"_id": False})
    velog_urls = []
    for mem in velog_mem:
        if mem["blog"].strip():
            velog_urls.append((mem['username'], mem['blog'], mem["blog_type"]))
    for name, url, types in velog_urls:
        driver.get(url)
        scroll_to_bottom = "window.scrollTo(0, document.body.scrollHeight);"
        get_window_height = "return document.body.scrollHeight"
        last_height = driver.execute_script(get_window_height)
        while True:
            driver.execute_script(scroll_to_bottom)
            time.sleep(1)
            new_height = driver.execute_script(get_window_height)
            if new_height == last_height:
                break
            last_height = new_height
        contents = driver.find_elements(By.XPATH, '//*[@id="root"]/div[2]/div[3]/div[4]/div[3]/div/div/a')
        url_list =[]
        for content in contents:
            url_list.append(content.get_attribute('href'))
            students.update_one({"username": name}, {"$set": {"blog_list": sorted(url_list)}}, upsert=True)


if __name__ == '__main__':
    tistory_blog()