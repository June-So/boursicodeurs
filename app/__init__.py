from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object(Config)
migrate = Migrate(app, db)

from app import views, views_model, views_database, views_bot, models

#migrate.init_app(app, db)
