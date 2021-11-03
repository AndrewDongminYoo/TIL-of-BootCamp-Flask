from selenium.common.exceptions import NoSuchElementException
from datetime import datetime, timedelta, timezone
from selenium.webdriver.common.by import By
from pymongo import MongoClient
from selenium import webdriver
from db_insert import Post
import os
import re

os.popen("mongod")
client = MongoClient()
db = client.get_database("dbmember")
col1 = db.get_collection("student")
col2 = db.get_collection("articles")
members_blogs = col1.find({}).sort("blog_type")


def crawl_post():
    driver = webdriver.Chrome()
    for student in members_blogs:
        if student.get("blog_list"):
            if student["blog_type"] == "tistory":
                for url in student["blog_list"]:
                    if list(col2.find({"url": url})):
                        continue
                    try:
                        driver.get(url)
                        title = driver.find_element(By.CSS_SELECTOR, 'meta[property="og:title"]').get_attribute('content')
                        author = driver.find_element(By.CSS_SELECTOR, 'meta[property="og:article:author"]').get_attribute('content')
                        site_name = driver.find_element(By.CSS_SELECTOR, 'meta[property="og:site_name"]').get_attribute('content')
                        reg_date = driver.find_element(By.CSS_SELECTOR, 'meta[property="og:regDate"]').get_attribute('content')
                        modified_time = driver.find_element(By.CSS_SELECTOR, 'meta[property="article:modified_time"]').get_attribute('content')
                        image = driver.find_element(By.CSS_SELECTOR, 'meta[property="og:image"]').get_attribute('content')
                        description = driver.find_element(By.CSS_SELECTOR, 'meta[property="og:description"]').get_attribute('content')

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
                    except NoSuchElementException:
                        pass
            else:
                for url in student["blog_list"]:
                    if list(col2.find({"url": url})):
                        continue
                    try:
                        driver.get(url)
                        title = driver.title
                        author = driver.find_element(By.CSS_SELECTOR, 'span.username').text
                        site_name = driver.find_element(By.CSS_SELECTOR, 'a.user-logo').text
                        reg_date = driver.find_element(By.CSS_SELECTOR, 'div.information > span:nth-child(3)').text
                        image = driver.find_element(By.CSS_SELECTOR, 'meta[property="og:image"]').get_attribute('content')
                        description = driver.find_element(By.CSS_SELECTOR, 'meta[property="og:description"]').get_attribute('content')
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
                    except NoSuchElementException:
                        pass
    driver.quit()


def get_time(time_string) -> datetime:
    timezone(timedelta(hours=+9))
    regex0 = re.compile(r"[약 ]*(\d{1,2})일 전")
    regex00 = re.compile(r"[약 ]*(\d{1,2})시간 전")
    regex1 = re.compile(r"(\d{4})년 (\d{1,2})월 (\d{1,2})일")
    regex2 = re.compile(r"(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})")
    if time_string == "어제":
        return datetime.now() - timedelta(days=1)
    if regex0.match(time_string):
        n = int(regex0.match(time_string).groups()[0])
        return datetime.now() - timedelta(days=n)
    elif regex00.match(time_string):
        n = int(regex00.match(time_string).groups()[0])
        return datetime.now() - timedelta(hours=n)
    elif regex1.match(time_string):
        year, month, day = map(int, regex1.match(time_string).groups())
        return datetime(year, month, day)
    elif regex2.match(time_string):
        year, month, day, hour, minute, sec = map(int, regex2.match(time_string).groups())
        return datetime(year, month, day, hour, minute, sec)
    else:
        return datetime.fromisoformat(time_string)


def put_doc(post):
    col2.update_one({"url": post['url']}, {"$set": post.to_mongo()}, upsert=True)


if __name__ == '__main__':
    crawl_post()
