# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify
from pymongo import MongoClient
import os

os.popen("mongod")
client = MongoClient()
db = client.get_database("dbmember")
col1 = db.get_collection("student")
col3 = db.get_collection("members")
col2 = db.get_collection("articles")
bp = Blueprint(name="api", import_name="api", url_prefix="/api")


@bp.route("/rank")
def get_list_of_blogs():
    members = list(col1.find({}, {"_id": False}))
    for mem in members:
        if not mem.get('blog_list'):
            members.remove(mem)
    members.sort(key=lambda x: (-len(x['blog_list'])))
    result = {}
    for ranker in members:
        r = db.get_collection("members").find_one({"username": ranker["username"]}, {"_id": False})
        result[len(ranker["blog_list"])] = r
    return jsonify(result)


@bp.route("/notion_naver_medium")
def get_list_of_unknown_blogs():
    result1 = list(col1.find({"blog_type": "medium"}, {"_id": False}))
    result2 = list(col1.find({"blog_type": "naver"}, {"_id": False}))
    result3 = list(col1.find({"blog_type": "notion"}, {"_id": False}))
    students = result1+result2+result3
    result = []
    for std in students:
        result.extend(list(col3.find({"username": std["username"]}, {"_id": False})))
    return jsonify(result)


@bp.route("/list")
def get_list_of_posts():
    post_list = list(col2.find({}, {"_id": False}).sort('registered', -1).limit(50))
    return jsonify(post_list)
