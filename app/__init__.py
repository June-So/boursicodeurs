from flask import Flask
from SECRET import *

app = Flask(__name__)
app.config['SECRET_KEY'] = FLASK_SECRET_KEY
from app import views