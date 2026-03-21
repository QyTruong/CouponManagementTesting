import hashlib
from datetime import datetime
import cloudinary.uploader
from sqlalchemy.exc import IntegrityError
from app import app, db, utils
from app.models import Coupon, UserRole, CouponType, User


def load_coupon():
    query = Coupon.query

    return query.all()

def create_coupon(data, role):
    if role is not UserRole.ADMIN:
        raise ValueError('Chỉ có admin mới có thể tạo phiếu giảm giá')
    if Coupon.query.filter(Coupon.code.__eq__(data['code'])).first():
        raise ValueError('Mã phiếu giảm này đã tồn tại')
    if data['expiry_date'] <= datetime.now():
        raise ValueError('Thời hạn sử dụng phải sau ngày giờ hiện tại')
    if data['max_quantity'] <= 0:
        raise ValueError('Số lượng phiếu phải lớn hơn 0')
    if data['value'] <= 0:
        raise ValueError('Giá trị giảm phải lớn hơn 0')
    if data['coupon_type'] == CouponType.VARIABLE and data['value'] > 50:
        raise ValueError('Phiếu giảm giá với hình thức % không được vượt quá 50%')
    if data['coupon_type'] == CouponType.FIXED and data['value'] < 1000:
        raise ValueError('Mệnh giá này không tồn tại')

    c = Coupon(code=data['code'], value=data['value'], coupon_type=data['coupon_type'], max_quantity=data['max_quantity'], expiry_date=data['expiry_date'])

    db.session.add(c)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise Exception('Mã này đã tồn tại')

def add_user(name, username, password, avatar=None):
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

