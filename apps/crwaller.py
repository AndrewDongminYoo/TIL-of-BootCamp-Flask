from pymongo import MongoClient
import mongoengine as me
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import csv
from pprint import pprint
import os
os.popen("mongod")
client = MongoClient()
db = client.get_database("dbmember")
members = db.get_collection("student").find({"blog_type": "tistory"}, {"_id": False})
tistory_urls = []

for member in members:
    if member["blog"].strip():
        tistory_urls.append((member['username'], member['blog'], member["blog_type"]))
pprint(tistory_urls)

for name, url, types in tistory_urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.select_one('meta[property="og:title"]')['content']
    image = soup.select_one('meta[property="og:image"]')['content']
    description = soup.select_one('meta[property="og:description"]')['content']
    print(soup.select_one("head"))
    break
    # print(title, image, description)