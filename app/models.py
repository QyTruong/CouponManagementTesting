from datetime import datetime
from sqlalchemy import Integer, Column, String, Boolean, DateTime, Enum, Float, ForeignKey
from sqlalchemy.orm import relationship
from app import app, db
from enum import Enum as Type

class UserRole(Type):
    ADMIN = 1
    USER = 2

class CouponType(Type):
    FIXED = 1
    VARIABLE = 2

class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True)


class User(BaseModel):
    __tablename__ = 'user'

    active = Column(Boolean, default=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    avatar = Column(String(50), nullable=False)
    joined_date = Column(DateTime, default=datetime.now)

    orders = relationship('Order', backref='user', lazy=True)

    def __str__(self):
        return self.name

class Coupon(BaseModel):
    __tablename__ = 'coupon'

    code = Column(String(50), nullable=False)
    value = Column(Float, default=0)
    coupon_type = Column(Enum(CouponType), default=CouponType.FIXED)
    availability_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    expiry_date = Column(DateTime, nullable=False)

    orders = relationship('Order', backref='coupon', lazy=True)

    def __str__(self):
        return self.code

class Order(BaseModel):
    __tablename__ = 'order'

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    coupon_id = Column(Integer, ForeignKey('coupon.id'), nullable=True)
    total_price = Column(Float, default=0)
    discount = Column(Float, default=0)
    final_price = Column(Float, default=0)
    created_at = Column(DateTime, default=datetime.now)

    details = relationship('OrderDetail', backref='order', lazy=True)

class OrderDetail(BaseModel):
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)


class Product(BaseModel):
    __tablename__ = 'product'

    name = Column(String(50), nullable=False)
    price = Column(Float, default=0)
    image = Column(String(100), nullable=False)

    details = relationship('OrderDetail', backref='product', lazy=True)

    def __str__(self):
        return self.name

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
