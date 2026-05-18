from datetime import datetime, timedelta

from app import db
from app.dao.dao_coupon import load_coupon_by_code
from app.test.test_base import (test_app, test_session, test_client, sample_coupons,
                                sample_coupon_users, mock_login, sample_users, sample_products)
import pytest
from app.models import CouponType, Coupon
from app.dao.dao_order import add_order


def set_cart_and_coupon(test_client, cart, code, value, coupon_type):
    with test_client.session_transaction() as sess:
        sess['cart'] = cart
        if code:
            sess['coupon_slot'] = {
                'code': code,
                'value': value,
                'coupon_type': coupon_type
            }


def test_order_success_without_coupon(test_client, sample_coupons, sample_products, mock_login, mocker):
    class FakeOrder:
        def __init__(self):
            self.coupon_id = None

    mocker.patch("app.index.add_order", return_value=FakeOrder())
    mocker.patch("app.index.utils.stats_cart", return_value= {
        "total_price": 20000, "discount_value": 0, "final_price": 20000
    })

    with test_client.session_transaction() as sess:
        sess['cart'] = {
            "1": {'id': 1, 'quantity': 2, 'price': 10000},
        }

    res = test_client.post('/api/order')
    data = res.get_json()

    assert res.status_code == 200
    assert data['status'] == 200
    assert data['coupon_err_msg'] is None

    with test_client.session_transaction() as sess:
        assert  'cart' not in sess
        assert 'coupon_slot' not in sess


def test_order_success_with_valid_coupon( test_client, sample_coupons,sample_products, mock_login, mocker):
    class FakeOrder:
        def __init__(self):
            self.coupon_id = None

    mocker.patch("app.index.add_order", return_value=FakeOrder())

    mocker.patch("app.index.utils.stats_cart", return_value={
        "total_price": 20000,
        "discount_value": 0,
        "final_price": 20000
    })
    mocker.patch("app.index.apply_coupon")

    set_cart_and_coupon(test_client, cart={'1': {'id': 1, 'price': 30000, 'quantity': 2}},
                         code='SALE10',value=10000,coupon_type=CouponType.FIXED.value)

    res = test_client.post('/api/order')
    data = res.get_json()

    assert data['status'] == 200
    assert data['coupon_err_msg'] is None


def test_order_coupon_expired(test_client, sample_coupons, sample_products, mock_login, mocker, test_session):

    class FakeOrder:
        def __init__(self):
            self.coupon_id = None
            self.total_price = 60000
            self.discount = 0
            self.final_price = 60000
            self.coupon = None

    mocker.patch("app.index.add_order", return_value=FakeOrder())

    mocker.patch("app.index.utils.stats_cart", return_value={
        "total_price": 60000,
        "discount_value": 0,
        "final_price": 60000
    })

    # bypass permission
    mocker.patch("app.dao.dao_coupon.validate_usage_limitation")

    coupon = Coupon.query.filter_by(code='SALE20').first()
    coupon.expiry_date = datetime.now() - timedelta(days=1)

    test_session.commit()

    set_cart_and_coupon( test_client,
        cart={
            '1': {
                'id': 1,
                'price': 30000,
                'quantity': 2
            }
        },
        code='SALE20',
        value=10000,
        coupon_type=CouponType.FIXED.value
    )

    res = test_client.post('/api/order')
    data = res.get_json()

    assert data['status'] == 200
    assert 'hết hạn' in data['coupon_err_msg']


def test_order_coupon_usage_limit(test_client, sample_coupons, sample_products, mock_login, mocker):

    class FakeOrder:
        def __init__(self):
            self.coupon_id = None
            self.total_price = 60000
            self.discount = 0
            self.final_price = 60000
            self.coupon = None

    mocker.patch("app.index.add_order",return_value=FakeOrder())

    mocker.patch( "app.index.utils.stats_cart",return_value={
                                                "total_price": 60000,
                                                "discount_value": 0,
                                                "final_price": 60000
                            })

    mocker.patch("app.dao.dao_coupon.validate_usage_limitation",
                side_effect=ValueError("Mã giảm giá đã vượt quá số lần sử dụng cho phép"))

    with test_client.session_transaction() as sess:
        sess['cart'] = {
            '1': {
                'id': 1,
                'price': 30000,
                'quantity': 2
            }
        }

        sess['coupon_slot'] = {
            'code': 'SALE20'
        }

    res = test_client.post('/api/order')
    data = res.get_json()

    assert data['status'] == 200
    assert 'quá số lần' in data['coupon_err_msg']



