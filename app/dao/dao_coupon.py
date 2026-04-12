from sqlite3 import IntegrityError
from flask_login import current_user
from sqlalchemy import func
from app import db
from app.models import Coupon, UserRole, CouponType, Order, OrderStatus
from datetime import datetime, timedelta


# Tạo mã giảm giá
def create_coupon(code, value, coupon_type, max_quantity, expiry_date, role):
    if role is not UserRole.ADMIN:
        raise ValueError('Chỉ có admin mới có thể tạo phiếu giảm giá')

    validate_expiration(expiry_date=expiry_date)
    validate_quantity(max_quantity=max_quantity)
    validate_value(value=value, coupon_type=coupon_type)

    if Coupon.query.filter(Coupon.code.__eq__(code)).first():
        raise ValueError('Mã phiếu giảm này đã tồn tại')

    c = Coupon(code=code, value=value, coupon_type=coupon_type, max_quantity=max_quantity, expiry_date=expiry_date)

    db.session.add(c)
    try:
        db.session.commit()
        return c
    except IntegrityError as ex:
        db.session.rollback()
        raise Exception(ex)


def validate_expiration(expiry_date):
    now = datetime.now()

    if expiry_date <= now:
        raise ValueError('Thời hạn sử dụng phải sau ngày giờ hiện tại')

    if expiry_date < now + timedelta(days=1):
        raise ValueError('Thời hạn sử dụng phải lớn hơn ít nhất 1 ngày')

def validate_quantity(max_quantity):
    if max_quantity <= 0:
        raise ValueError('Số lượng phiếu phải lớn hơn 0')
    if max_quantity > 500:
        raise ValueError('Số lượng không được vượt quá 500')

def validate_value(value, coupon_type):
    if value <= 0:
        raise ValueError('Giá trị giảm phải lớn hơn 0')

    if coupon_type == CouponType.FIXED and value > 500000:
        raise ValueError('Không được vượt quá 500.000 VND')

    if coupon_type == CouponType.FIXED and value < 1000:
        raise ValueError('Mệnh giá này không tồn tại')

    if coupon_type == CouponType.VARIABLE and value > 50:
        raise ValueError('Phiếu giảm giá với hình thức % không được vượt quá 50%')

def load_coupon_by_code(code):
    return Coupon.query.filter(Coupon.code.__eq__(code)).first()

# Áp dụng mã giảm giá
def apply_coupon(order, coupon):
    if coupon.expiry_date > datetime.now():
        raise ValueError('Mã này đã hết hạn sử dụng, áp dụng mã thất bại')
    if order.coupon_id is not None:
        raise ValueError('Đơn hàng này đã được áp dụng mã giảm giá từ trước, áp dụng mã thất bại')

    discount_value = 0

    if coupon.coupon_type == CouponType.FIXED:
        discount_value = coupon.value
    elif coupon.coupon_type == CouponType.VARIABLE:
        discount_value = (order.total_price * (coupon.value/100))
    order.discount = discount_value

    final_price = order.total_price - discount_value
    order.final_price = final_price if final_price >= 0 else 0

    order.coupon = coupon

    db.session.commit()

# Xóa mã giảm giá
def delete_coupon(coupon, role):
    if role is not UserRole.ADMIN:
        raise ValueError("Chỉ có admin mới được xóa mã giảm giá")

    validate_order_in_processing(coupon=coupon)

    coupon.active = False
    db.session.commit()


def validate_order_in_processing(coupon):
    if Order.query.filter(Order.coupon_id.__eq__(coupon.id),
                            Order.status.__eq__(OrderStatus.PROCESSING)).first():
        raise ValueError("Không thể xóa mã giảm giá này, vì vẫn đang tồn tại đơn hàng đang xử lý")



def load_coupons(kw=None):
    query = Coupon.query.filter(Coupon.active==True)

    if kw:
        query = query.filter(Coupon.code.contains(kw))

    return query.all()

def count_used_coupons():
    query = db.session.query(Order.coupon_id, func.count(Order.id))\
            .filter(Order.coupon_id.isnot(None))\
            .group_by(Order.coupon_id)
    return query.all()

def count_used_coupon(id):
    return db.session.query(Order.coupon_id, func.count(Order.id))\
                    .filter(Order.coupon_id==id)\
                    .group_by(Order.coupon_id).first()
