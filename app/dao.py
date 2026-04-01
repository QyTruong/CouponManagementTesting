import hashlib
from datetime import datetime
import cloudinary.uploader
from flask_login import current_user
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from app import app, db
from app.models import Coupon, UserRole, CouponType, User, Product, Category, Order, OrderDetail


def load_coupon():
    query = Coupon.query

    return query.all()


# Tạo mã giảm giá
def create_coupon(code, value, coupon_type, max_quantity, expiry_date, role):
    if role is not UserRole.ADMIN:
        raise ValueError('Chỉ có admin mới có thể tạo phiếu giảm giá')
    if Coupon.query.filter(Coupon.code==code).first():
        raise ValueError('Mã phiếu giảm này đã tồn tại')
    if expiry_date <= datetime.now():
        raise ValueError('Thời hạn sử dụng phải sau ngày giờ hiện tại')
    if max_quantity <= 0:
        raise ValueError('Số lượng phiếu phải lớn hơn 0')
    if value <= 0:
        raise ValueError('Giá trị giảm phải lớn hơn 0')
    if coupon_type == CouponType.VARIABLE and value > 50:
        raise ValueError('Phiếu giảm giá với hình thức % không được vượt quá 50%')
    if coupon_type == CouponType.FIXED and value < 1000:
        raise ValueError('Mệnh giá này không tồn tại')

    c = Coupon(code=code, value=value, coupon_type=coupon_type, max_quantity=max_quantity, expiry_date=expiry_date)

    db.session.add(c)
    try:
        db.session.commit()
        return c
    except IntegrityError as ex:
        db.session.rollback()
        raise Exception(ex)

def load_products(kw=None, category_id=None, page=1):
    query = Product.query

    if kw:
        query = query.filter(Product.name.contains(kw))

    if category_id:
        query = query.filter(Product.category_id == category_id)

    if page:
        start = (page - 1) * app.config['PAGE_SIZE']
        query = query.slice(start, start + app.config['PAGE_SIZE'])

    return query.all()


def count_products():
    return Product.query.count()


def load_categories():
    query = Category.query
    return query.all()

def load_coupons(kw=None):
    query = Coupon.query.filter(Coupon.active==True)

    if kw:
        query = query.filter(Coupon.code.contains(kw))

    return query.all()

def count_used_coupons():
    query = db.session.query(Order.coupon_id, func.count(Order.id))\
            .group_by(Order.coupon_id)
    return query.all()

def count_used_coupon(id):
    return db.session.query(Order.coupon_id, func.count(Order.id))\
                    .filter(Order.coupon_id==id)\
                    .group_by(Order.coupon_id).first()

def get_coupon_by_code(code):
    return Coupon.query.filter(Coupon.code==code).first()


# Áp dụng mã giảm giá
def apply_coupon(code, coupon_slot):
    if not current_user.is_authenticated:
        raise ValueError('Bạn phải đăng nhập để có thể sử dụng phiếu giảm giá')

    if coupon_slot:
        raise ValueError('Mỗi đơn hàng chỉ được áp dụng 1 mã duy nhất, vui lòng hãy gỡ mã đã áp dụng trước đó')

    coupon = get_coupon_by_code(code=code)

    if coupon:
        if datetime.now() > coupon.expiry_date:
            raise ValueError('Mã này hiện đã hết hạn, không áp dụng được')

        coupon_count = count_used_coupon(id=coupon.id)

        if coupon_count[1] >= coupon.max_quantity:
            raise ValueError('Mã giảm giá này đã hết, không thể sử dụng được')
    else:
        raise ValueError('Mã này không tồn tại')

    return coupon



def add_order(cart, cart_stats, coupon=None):
    if cart:
        total_price = cart_stats['base_price']
        discount = cart_stats['discount_value']
        final_price = cart_stats['total_price']

        o = Order(user=current_user, coupon=coupon, total_price=total_price, discount=discount, final_price=final_price)
        db.session.add(o)

        for ca in cart.values():
            d = OrderDetail(quantity=ca['quantity'], price=ca['price'], product_id=ca['id'], order=o)
            db.session.add(d)

        db.session.commit()

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


def get_user_by_id(id):
    return User.query.get(id)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username==username, User.password==password).first()