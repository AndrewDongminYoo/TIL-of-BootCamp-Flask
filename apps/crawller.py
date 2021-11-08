# -*- coding: utf-8 -*-
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime, timedelta, timezone
from selenium.webdriver.common.by import By
from pymongo.collection import Collection
from pymongo import MongoClient
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib import parse
import mongoengine as me
import schedule
import uuid
import csv
import time
import re
import os

client = MongoClient("mongodb://admin:rew748596@3.35.149.46:27017/")
db = client.get_database("member_card")
articles = db.get_collection("articles")
members = db.get_collection("members")
members_blogs = members.find({}).sort("blog_type")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--single-process")
chrome_options.add_argument("--disable-dev-shm-usage")
# path = "./chromedriver"
path = __path__


class Member(me.Document):
    uid = me.UUIDField(binary=False)
    username = me.StringField()
    blog = me.URLField()
    blog_type = me.StringField()
    image = me.URLField()
    member_card = me.StringField()
    hobby = me.ListField()
    specialty = me.ListField()


class Post(me.Document):
    name = me.StringField()
    author = me.StringField()
    title = me.StringField()
    site_name = me.StringField()
    description = me.StringField()
    url = me.URLField()
    image = me.URLField()
    registered = me.DateTimeField()
    modified = me.DateTimeField()
    shared = me.IntField()
    comment = me.IntField()


def inject_members():
    with open("data/blog.csv", newline="",
              encoding="utf-8", mode="r") as input_file:
        input_file.__next__()
        for line in input_file.readlines():
            [name, blog, x, btype] = line.strip().split(',')
            print(blog)
            if blog:
                mem = Member(
                    uid=uuid.uuid4(),
                    username=name,
                    blog=blog,
                    blog_type=btype
                )
                members.update_one({"username": name}, {'$set': mem.to_mongo()}, upsert=True)


def member_card():
    with open("data/member.csv", newline="",
              encoding="utf-8", mode="r") as input_file:
        input_file.__next__()
        reader = csv.reader(input_file)
        for line in reader:
            [name, blog, hobby, specialty] = line[:4]
            hobby = hobby.replace(', ', ',')
            hobby = hobby.replace(', ', ',')
            specialty = specialty.replace(', ', ',')
            specialty = specialty.replace(', ', ',')
            image = ""
            for f in os.listdir("../static/img"):
                if f.startswith(name):
                    image = f
            mem = Member(
                username=name,
                image="/static/img/" + image,
                blog=blog,
                hobby=hobby.split(','),
                specialty=specialty.split(','))
            members.update_one({"username": name}, {'$set': mem.to_mongo()}, upsert=True)


def tistory_blog():
    print("daum-tistory blog detected")
    driver = webdriver.Chrome(path, chrome_options=chrome_options)
    tistory_members = members.find({"blog_type": "tistory"}, {"_id": False})
    tistory_urls = []
    for member in tistory_members:
        if member["blog"].strip():
            tistory_urls.append((member['username'], member['blog'], member["blog_type"]))
    for name, url, types in tistory_urls:
        target_part = parse.urlparse(url + "sitemap")
        target = parse.urlunparse(target_part)
        driver.get(target)
        res = driver.page_source
        soup = BeautifulSoup(res, 'html.parser')
        regex = re.compile(url + r"\d+")
        url_list = sorted(regex.findall(soup.text))
        if not url_list:
            regex = re.compile(url + "entry/" + r"[\-%\w\d]+")
            url_list = sorted(regex.findall(soup.text))
        members.update_one({"username": name}, {"$set": {"blog_list": sorted(list(set(url_list)))}}, upsert=True)
    driver.quit()


def github_blog():
    print("github.io blog detected")
    driver = webdriver.Chrome(path, chrome_options=chrome_options)
    github_members = members.find({"blog_type": "github"}, {"_id": False})
    github_urls = []
    for member in github_members:
        if member["blog"].strip():
            github_urls.append((member['username'], member['blog'], member["blog_type"]))
    for name, url, types in github_urls:
        target_part = parse.urlparse(url + "sitemap")
        target = parse.urlunparse(target_part)
        driver.get(target)
        res = driver.page_source
        soup = BeautifulSoup(res, 'html.parser')
        regex = re.compile(url + r"[^pagets][\d\-/TILa-z]+")
        url_list = sorted(regex.findall(soup.text))
        members.update_one({"username": name}, {"$set": {"blog_list": sorted(list(set(url_list)))}}, upsert=True)
    driver.quit()


def velog_blog():
    print("velo-pert blog detected")
    driver = webdriver.Chrome(path, chrome_options=chrome_options)
    velog_members = members.find({"blog_type": "velog"}, {"_id": False})
    velog_urls = []
    for mem in velog_members:
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
        url_list = []
        for content in contents:
            url_list.append(content.get_attribute('href'))
        members.update_one({"username": name}, {"$set": {"blog_list": sorted(list(set(url_list)))}}, upsert=True)
    driver.quit()


def crawl_post():
    print("let's crawl!!!!!")
    driver = webdriver.Chrome(path, chrome_options=chrome_options)
    for student in members_blogs:
        if student.get("blog_list"):
            blog_list = list(set(student["blog_list"]))
            members.update_one({"username": student["username"]}, {"$set": {"blog_list": blog_list}})
            if student["blog_type"] == "tistory" or student["blog_type"] == "github":
                for url in blog_list:
                    if list(articles.find({"url": url})):
                        continue
                    try:
                        driver.get(url)
                        title = driver.find_element(By.CSS_SELECTOR, 'meta[property="og:title"]') \
                            .get_attribute('content')
                        author = driver.find_element(By.CSS_SELECTOR, 'meta[property="og:article:author"]') \
                            .get_attribute('content')
                        site_name = driver.find_element(By.CSS_SELECTOR, 'meta[property="og:site_name"]') \
                            .get_attribute('content')
                        reg_date = driver.find_element(By.CSS_SELECTOR, 'meta[property="og:regDate"]') \
                            .get_attribute('content')
                        modified_time = driver.find_element(By.CSS_SELECTOR, 'meta[property="article:modified_time"]') \
                            .get_attribute('content')
                        image = driver.find_element(By.CSS_SELECTOR, 'meta[property="og:image"]') \
                            .get_attribute('content')
                        description = driver.find_element(By.CSS_SELECTOR, 'meta[property="og:description"]') \
                            .get_attribute('content')

                        post = Post(
                            name=student['username'],
                            author=author,
                            url=url,
                            title=title,
                            site_name=site_name,
                            registered=get_time(reg_date),
                            modified=get_time(modified_time),
                            image=image,
                            description=description,
                            shared=0,
                            comment=0
                        )
                        put_doc(post)
                        print(get_time(reg_date))
                    except NoSuchElementException:
                        pass
            else:
                for url in blog_list:
                    if list(articles.find({"url": url})):
                        continue
                    try:
                        driver.get(url)
                        title = driver.title
                        author = driver.find_element(By.CSS_SELECTOR, 'span.username').text
                        site_name = driver.find_element(By.CSS_SELECTOR, 'a.user-logo').text
                        reg_date = driver.find_element(By.CSS_SELECTOR, 'div.information > span:nth-child(3)').text
                        image = driver.find_element(By.CSS_SELECTOR, 'meta[property="og:image"]') \
                            .get_attribute('content')
                        description = driver.find_element(By.CSS_SELECTOR, 'meta[property="og:description"]') \
                            .get_attribute('content')
                        post = Post(
                            name=student['username'],
                            author=author,
                            url=url,
                            title=title,
                            site_name=site_name,
                            registered=get_time(reg_date),
                            image=image,
                            description=description,
                            shared=0,
                            comment=0
                        )
                        put_doc(post)
                        print(get_time(reg_date))
                    except NoSuchElementException:
                        pass
    driver.quit()


def get_time(time_string):
    timezone(timedelta(hours=+9))
    regex0 = re.compile(r"[약 ]*(\d{1,2})일 전")
    regex00 = re.compile(r"[약 ]*(\d{1,2})시간 전")
    regex000 = re.compile(r"[약 ]*(\d{1,2})분 전")
    regex0000 = re.compile(r"[약 ]*(\d{1,2})초 전")
    regex1 = re.compile(r"(\d{4})년 (\d{1,2})월 (\d{1,2})일")
    regex2 = re.compile(r"(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})")
    regex02 = re.compile(r"(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})\+09:00")
    if time_string == "어제":
        return datetime.now() - timedelta(days=1)
    if regex0.match(time_string):
        n = int(regex0.match(time_string).groups()[0])
        return datetime.now() - timedelta(days=n)
    elif regex00.match(time_string):
        n = int(regex00.match(time_string).groups()[0])
        return datetime.now() - timedelta(hours=n)
    elif regex000.match(time_string):
        n = int(regex000.match(time_string).groups()[0])
        return datetime.now() - timedelta(minutes=n)
    elif regex0000.match(time_string):
        n = int(regex0000.match(time_string).groups()[0])
        return datetime.now() - timedelta(seconds=n)
    elif regex1.match(time_string):
        year, month, day = map(int, regex1.match(time_string).groups())
        return datetime(year, month, day)
    elif regex2.match(time_string):
        year, month, day, hour, minute, sec = map(int, regex2.match(time_string).groups())
        return datetime(year, month, day, hour, minute, sec)
    else:
        year, month, day, hour, minute, sec = map(int, regex02.match(time_string).groups())
        return datetime(year, month, day, hour, minute, sec)


def put_doc(post):
    print(post.description)
    articles.update_one({"url": post['url']}, {"$set": post.to_mongo()}, upsert=True)


def main():
    print("hi", datetime.now())
    inject_members()
    member_card()
    tistory_blog()
    github_blog()
    velog_blog()
    crawl_post()


if __name__ == '__main__':
    main()
    schedule.every().hours.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
    # main()
