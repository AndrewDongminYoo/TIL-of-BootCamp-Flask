# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify
from pymongo import MongoClient
import os

client = MongoClient(os.environ.get('DB_PATH'))
if client.HOST == 'localhost':
    os.popen("mongod")
db = client.get_database("member_card")
col1 = db.get_collection("members")
col2 = db.get_collection("articles")
bp = Blueprint(name="api", import_name="api", url_prefix="/api")


@bp.route("/rank")
def get_list_of_blogs():
    members = list(col1.find({}, {"_id": False}).sort("blog_list", -1))
    for mem in members:
        if not mem.get('blog_list'):
            members.remove(mem)
    result = {}
    for ranker in members:
        r = db.get_collection("members").find_one({"username": ranker["username"]}, {"_id": False})
        if ranker.get("blog_list"):
            result[len(ranker.get("blog_list"))] = r
    return jsonify(result)


@bp.route("/notion_naver_medium")
def get_list_of_unknown_blogs():
    result1 = list(col1.find({"blog_type": "medium"}, {"_id": False}))
    result2 = list(col1.find({"blog_type": "naver"}, {"_id": False}))
    result3 = list(col1.find({"blog_type": "notion"}, {"_id": False}))
    students = result1+result2+result3
    return jsonify(students)


@bp.route("/list")
def get_list_of_posts():
    post_list = list(col2.find({}, {"_id": False}).sort('registered', -1).limit(50))
    return jsonify(post_list)
