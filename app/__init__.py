import os
import json
from flask import Flask
from flask_cors import CORS
from flask_mongoengine import MongoEngine

app = Flask(__name__, static_folder='react_app')
CORS(app)

# init mongo
mongo_user = os.environ['MONGO_USER']
mongo_pw = os.environ['MONGO_PW']
mongo_db = os.environ['MONGO_DB']
mongo_host = os.environ.get('MONGO_HOST', 'localhost')
app.config['MONGODB_SETTINGS'] = {
    'username': mongo_user,
    'password': mongo_pw,
    'host': mongo_host,
    'db': mongo_db
}
db = MongoEngine()
db.init_app(app)

app_secret_key = os.environ['APP_SECRET_KEY']
app.secret_key = bytes(app_secret_key, 'utf-8')

from app import routes
