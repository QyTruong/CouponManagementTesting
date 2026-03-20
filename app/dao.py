from datetime import datetime
from sqlalchemy.exc import IntegrityError
from app import app, db, utils
from app.models import Coupon, UserRole, CouponType


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
    if data['availability_count'] <= 0:
        raise ValueError('Số lượng phiếu phải lớn hơn 0')
    if data['value'] <= 0:
        raise ValueError('Giá trị giảm phải lớn hơn 0')
    if data['coupon_type'] == CouponType.VARIABLE and data['value'] > 50:
        raise ValueError('Phiếu giảm giá với hình thức % không được vượt quá 50%')

    c = Coupon(code=data['code'], value=data['value'], coupon_type=data['coupon_type'], availability_count=data['availability_count'], expiry_date=data['expiry_date'])

    db.session.add(c)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise Exception('Mã này đã tồn tại')