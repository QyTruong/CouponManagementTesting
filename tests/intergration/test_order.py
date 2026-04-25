from app.test.test_base import (test_app, test_session, test_client, sample_coupons,
                                sample_coupon_users, mock_login, sample_users, sample_products)
import pytest
from app.models import CouponType


def set_cart_and_coupon(test_client, cart, code, value, coupon_type):
    with test_client.session_transaction() as sess:
        sess['cart'] = cart
        if code:
            sess['coupon_slot'] = {
                'code': code,
                'value': value,
                'coupon_type': coupon_type
            }


# def test_order_success(test_client, sample_coupons, sample_products, mock_login, mocker):
#     class FakeOrder:
#         coupon_id = None
#
#     mocker.patch("app.dao.dao_order.add_order", return_value=FakeOrder())
#
#     set_cart_and_coupon(test_client, cart= {'1': {'id': 1, 'price': 10000, 'quantity': 2}},
#                         code='SALE10', value=10000, coupon_type=CouponType.FIXED.value)
#
#     res = test_client.post('/api/order')
#     data = res.get_json()
#
#     assert res.status_code == 200
#     assert data['status'] == 200
#     print(data)
#
#     assert data.get('coupon_err_msg') is None
#
#     with test_client.session_transaction() as sess:
#         assert  'cart' not in sess
#         assert 'coupon_slot' not in sess