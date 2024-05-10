from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

UPLOAD_FOLDER = 'MongoFlaskApp\store\static\img_urls'

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/your_database'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mongoDB = PyMongo(app)

from .route import *
                

