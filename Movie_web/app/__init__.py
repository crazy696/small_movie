# coding:utf8
import os
from flask import Flask, render_template
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
# from flask_wtf.csrf import CsrfProtect
import pymysql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:520@localhost:3306/movie_web_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = '9db192b57d0e4e4dba6dc661403ea0b0'
app.config['REDIS_URL'] = 'redis://localhost:6379/0'
app.config['UP_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads/')
app.config['FC_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads/Users/')
app.debug = False

db = SQLAlchemy(app)
rds = FlaskRedis(app)
# CsrfProtect(app)


from app.admin import admin as admin_blueprint
from app.home import home as home_blueprint

app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(home_blueprint)


@app.errorhandler(404)
def page_ont_found(error):
    return render_template('home/404.html'), 404
