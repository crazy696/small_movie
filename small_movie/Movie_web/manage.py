# coding:utf8
#! /home/crazy696/Documents/work/Virtual_environment/venv/bin/python3.6


from app import app
from flask_script import Manager

manage = Manager(app)

if __name__ == "__main__":
    manage.run()
