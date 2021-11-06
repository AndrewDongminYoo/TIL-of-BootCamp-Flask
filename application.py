# -*- coding: utf-8 -*-
from flask import Flask, render_template
from apis.api import bp

application = Flask(__name__)
application.register_blueprint(bp)


@application.route('/')
def hello_world():  # put application's code here
    return render_template("index.html")


@application.route('/search')
def explore_world():  # put application's code here
    return render_template("search.html")


if __name__ == '__main__':
    application.run()
