from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_login import LoginManager
import os
import cloudinary.uploader
import stripe

db = SQLAlchemy()
login = LoginManager()

def create_app(test_config=None):
    app = Flask(__name__)
    load_dotenv()

    app.secret_key = os.getenv('APP_SECRET_KEY')

    if test_config:
        app.config.update(test_config)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/coupondb?charset=utf8mb4'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['PAGE_SIZE'] = 6

    db.init_app(app=app)
    login.init_app(app=app)

    cloudinary.config(
        cloud_name=os.getenv('CLOUDINARY_NAME'),
        api_key=os.getenv('CLOUDINARY_API_KEY'),
        api_secret=os.getenv('CLOUDINARY_SECRET_KEY')
    )

    return app







