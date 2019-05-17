from flask import Flask
from SECRET import *

app = Flask(__name__)

from app import views