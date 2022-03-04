from flask import Flask, render_template, send_file, request
import os
import pymongo
from flask_pymongo import PyMongo
import datetime

app = Flask(__name__)

#setup mongo connection with database
app.config['MONGO_URI']="mongodb://localhost:27017/shows_db"
mongo = PyMongo(app)

#connect to collection
tv_shows = mongo.db.tv_shows

results= tv_shows.find()
for result in results:
    print(result)
