from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_login import LoginManager
import os
import cloudinary.uploader

db = SQLAlchemy()
login = LoginManager()

load_dotenv()

#pytest --cov=app --cov-report=term-missing

app = Flask(__name__)

app.secret_key = os.getenv('APP_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost/coupondb?charset=utf8mb4" #os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PAGE_SIZE'] = 6

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_SECRET_KEY')
)

db.init_app(app=app)
login.init_app(app=app)









