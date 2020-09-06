from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask_cors import *

app = Flask(__name__)
CORS(app, supports_credentials=True, resources=r'/*')
import os

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://myroot:1914571065@47.95.235.93:3306/sctu-ceeaa'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

app.config["SECRET_KEY"] = '235c749859ec44c2bd6064ec6da7b927'
app.config['EXPIRES_IN'] = 9999
app.config["UP_DIR"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/")
app.config['REDIS_HOST'] = 'localhost'
app.config['REDIS_PORT'] = 6379
app.config['REDIS_DB'] = '0'
app.config['REDIS_PWD'] = '1914571065'
app.debug = True
db = SQLAlchemy(app)

from app.home import home as home_blueprint
from app.permission.user import user as user_blueprint
from app.permission.menu import menu as menu_buleprint

app.register_blueprint(home_blueprint)
app.register_blueprint(user_blueprint, url_prefix="/user/")
app.register_blueprint(menu_buleprint, url_prefix="/menu/")
