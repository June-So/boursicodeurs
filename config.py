import os
from SECRET import *

database = 'mysql://{user}:{password}@{server}:{port}/{database}?charset=utf8mb4'.format(**DATABASE)
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = database
    MYSQL_DATABASE_CHARSET = 'utf8mb4'
    SECRET_KEY = FLASK_SECRET_KEY