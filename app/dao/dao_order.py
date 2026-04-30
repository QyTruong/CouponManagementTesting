from flask_login import current_user
from app import db
from app.models import Order, OrderDetail, OrderStatus


def load_order_by_id(id):
    return Order.query.filter(Order.id.__eq__(id)).first()


def add_order(cart, cart_stats):
    if cart:
        total_price = cart_stats['total_price']
        discount = cart_stats['discount_value']
        final_price = cart_stats['final_price']

        o = Order(user=current_user, total_price=total_price, discount=discount, final_price=final_price)
        db.session.add(o)

        for ca in cart.values():
            d = OrderDetail(quantity=ca['quantity'], price=ca['price'], product_id=ca['id'], order=o)
            db.session.add(d)

        db.session.commit()

        return o

    raise ValueError('Giỏ hàng không tồn tại')

def load_orders_by_user_id(user_id):
    return Order.query.filter(Order.user_id.__eq__(user_id)).all()


def pay_order(order_id):
    o = Order.query.filter(Order.id == order_id).first()

    if o is not None and o.status == OrderStatus.PROCESSING:
        o.status = OrderStatus.PAID
        db.session.commit()