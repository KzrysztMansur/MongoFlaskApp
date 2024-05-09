from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/your_database'

mongoDB = PyMongo(app)

from .route import *
                
