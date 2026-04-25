import pytest
from datetime import datetime, timedelta

from app import db
from app.dao.dao_coupon import delete_coupon
from app.models import Coupon, CouponType, Order, OrderStatus, User, UserRole
from app.test.test_base import test_app, test_session


def test_delete_coupon_success(test_session):
    coupon = Coupon(
        code="DEL_TEST",
        active=True,
        value=10000,
        coupon_type=CouponType.FIXED,
        expiry_date=datetime.now() + timedelta(days=30)
    )
    db.session.add(coupon)
    db.session.commit()

    assert coupon.active is True

    delete_coupon(coupon, role=UserRole.ADMIN)

    c = Coupon.query.filter(Coupon.code == "DEL_TEST").first()
    assert c.active is False


def test_delete_coupon_with_processing_order(test_session):
    # Tạo user giả lập
    user = User(name="User Test", username="usertest_del", password="123")
    db.session.add(user)

    # Tạo coupon giả lập
    coupon = Coupon(
        code="DEL_FAIL_TEST",
        active=True,
        value=10,
        coupon_type=CouponType.VARIABLE,
        expiry_date=datetime.now() + timedelta(days=30)
    )
    db.session.add(coupon)
    db.session.commit()

    order = Order(
        user_id=user.id,
        coupon_id=coupon.id,
        status=OrderStatus.PROCESSING,
        total_price=100000
    )
    db.session.add(order)
    db.session.commit()

    with pytest.raises(ValueError):
        delete_coupon(coupon, role=UserRole.ADMIN)

    c = Coupon.query.filter(Coupon.code == "DEL_FAIL_TEST").first()
    assert c.active is True
