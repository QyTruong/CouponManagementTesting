from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import cloudinary.uploader
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

app.secret_key = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_SECRET_KEY')
)


