from flask import Flask
from SECRET import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()
app.config['SECRET_KEY'] = FLASK_SECRET_KEY
from app import views
