# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request
from pymongo import MongoClient
import os

os.environ["DB_PATH"] = "mongodb://admin:rew748596@3.35.149.46:27017/member_card?authSource=admin"
client = MongoClient(os.environ.get('DB_PATH'))
db = client.get_database("member_card")
col1 = db.get_collection("members")
col2 = db.get_collection("articles")
bp = Blueprint(name="api", import_name="api", url_prefix="/api")


@bp.route("/rank")
def get_list_of_blogs():
    ranking = list(col1.find({}, {"_id": False}).sort("blog_list", -1))
    result = dict()
    for ranker in ranking:
        if ranker.get("blog_list"):
            result[len(ranker.get("blog_list"))] = ranker
    return jsonify(result)


@bp.route("/notion_naver_medium")
def get_list_of_unknown_blogs():
    result1 = list(col1.find({"blog_type": "medium"}, {"_id": False}))
    result2 = list(col1.find({"blog_type": "naver"}, {"_id": False}))
    result3 = list(col1.find({"blog_type": "notion"}, {"_id": False}))
    students = result1 + result2 + result3
    return jsonify(students)


@bp.route("/list")
def get_list_of_posts():
    query = request.args.get('query')
    if not query:
        post_list = list(col2.find({}, {"_id": False}).sort('registered', -1).limit(50))
    else:
        # col2.create_index({"$**": pymongo.TEXT})
        cursor = col2.find(
            {"$text": {"$search": query}},
            {"score": {"$meta": "textScore"},
             "_id": False})
        cursor.sort([("score", {"$meta": "textScore"})])
        post_list = list(cursor)
    return jsonify(post_list)


@bp.route("/none")
def coming_soon():
    cursor = col1.find({"blog": ""}, {"_id": False})
    result = []
    for member in list(cursor):
        result.append(member["username"])
    return jsonify(result)

