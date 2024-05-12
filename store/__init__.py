from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

UPLOAD_FOLDER = 'store\static\img_urls'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mongo_client = MongoClient('localhost', 27017)

from .routes import *
