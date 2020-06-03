import os
from flask import Flask
from flask_cors import CORS

app = Flask(__name__, static_folder='react_app')
CORS(app)


app_secret_key = os.environ['APP_SECRET_KEY']
app.secret_key = bytes(app_secret_key, 'utf-8')

from app import routes
