import hashlib
import re
from sqlite3 import IntegrityError

import cloudinary.uploader

from app import db
from app.models import User


def add_user(name, username, password, avatar=None):
    validate_name(name=name)
    validate_username(username=username)
    validate_password(password=password)

    if User.query.filter(User.username.__eq__(username)).first():
        raise ValueError('Tên đăng nhập này đã tồn tại, vui lòng đặt tên khác')

    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name.strip(), username=username.strip(), password=password)

    if avatar:
        resp = cloudinary.uploader.upload(avatar)
        u.avatar = resp['secure_url']

    db.session.add(u)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise Exception('Username này đã tồn tại')


def get_user_by_id(id):
    return User.query.get(id)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username==username, User.password==password).first()


def validate_name(name):
    if not name:
        raise ValueError("Không được để trống tên")

    if len(name) > 50:
        raise ValueError("Tên không quá 50 ký tự")

def validate_username(username):
    if not username:
        raise ValueError("Không được để trống tên đăng nhập")

    if len(username) < 4:
        raise ValueError("Tên đăng nhập phải tối thiểu 4 ký tự")

    if len(username) > 50:
        raise ValueError("Tên đăng nhập không được vượt quá 50 ký tự")


def validate_password(password):
    if not password:
        raise ValueError("Không được để trống mật khẩu")

    if len(password) < 8:
        raise ValueError("Mật khẩu tối thiểu 8 ký tự")

    if len(password) > 50:
        raise ValueError("Mật khẩu không được vượt quá 50 ký tự")

    if not re.search(r'[a-zA-Z]', password.strip()):
        raise ValueError("Mật khẩu phải có ít nhất 1 ký tự là chữ")

    if not re.search(r'[0-9]', password.strip()):
        raise ValueError("Mật khẩu phải có ít nhất 1 ký tự là số")
