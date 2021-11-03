from pymongo import MongoClient
import mongoengine as me
import uuid
import csv
import os
os.popen("mongod")
client = MongoClient()
db = client.get_database("dbmember")
col1 = db.get_collection("student")
col2 = db.get_collection("members")


class Member(me.Document):
    uid = me.UUIDField(binary=False)
    username = me.StringField()
    blog = me.URLField()
    blog_type = me.StringField()


class Student(me.Document):
    id = me.UUIDField(binary=False)
    username = me.StringField()
    url = me.URLField()
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
    input_file = open("../static/data/blog.csv", newline="", encoding="utf-8", mode="r")
    input_file.__next__()
    for line in input_file.readlines():
        [name, blog1, blog2, btype] = line.strip().split(',')
        if blog1:
            mem = Member(
                uid=uuid.uuid4().__str__(),
                username=name,
                blog=blog1,
                blog_type=btype
            )
            col1.update_one({"username": name}, {'$set': mem.to_mongo()})
        if blog2.strip():
            mem = Member(
                uid=uuid.uuid4().__str__(),
                username=name,
                blog=blog2,
                blog_type=btype
            )
            col1.update_one({"username": name}, {'$set': mem.to_mongo()})
    input_file.close()


def member_card():
    with open("../static/data/member.csv", newline="",
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
            mem = Student(
                username=name,
                image="/static/img/"+image,
                url=blog,
                hobby=hobby.split(','),
                specialty=specialty.split(',')
            )
            col2.update_one({"username": name}, {'$set': mem.to_mongo()})


if __name__ == '__main__':
    member_card()