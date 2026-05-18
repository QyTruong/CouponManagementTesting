from app.test.test_base import test_app, test_session, test_client, sample_coupons, sample_coupon_users, mock_login
import pytest
from app.utils import stats_cart


# def test_login_permission(test_client):
#     with test_client.session_transaction() as sess:
#         sess['cart'] = {
#             '1': {'price': 100000, 'quantity': 1}
#         }
#
#     res = test_client.post('/api/coupons', json={'code': 'SALE10'})
#     data = res.get_json()
#
#     assert data['err_msg'] == 'Đăng nhập để có thể sử dụng mã giảm giá'


def test_apply_coupon_after_login(test_client, sample_coupons, mock_login):

    with test_client.session_transaction() as sess:
        sess['cart'] = {
            '1': {'price': 100000, 'quantity': 1}
        }

    res = test_client.post('/api/coupons', json={'code': 'SALE10'})

    assert res.status_code == 200


def test_apply_coupon_no_cart(test_client, sample_coupons, mocker):
    class FakeUser:
        is_authenticated = True

    mocker.patch("flask_login.utils._get_user", return_value=FakeUser())

    res = test_client.post("/api/coupons", json={"code": "SALE20"})
    data = res.get_json()

    assert data['status'] == 404
    assert data['err_msg'] == 'Giỏ hàng không tồn tại'


def test_apply_coupon_success(test_client, sample_coupons, mocker):
    class FakeUser:
        is_authenticated = True

    mocker.patch("flask_login.utils._get_user", return_value=FakeUser())

    with test_client.session_transaction() as sess:
        sess['cart'] = {
            '1': {
                "price": 20000,
                "quantity": 2
            }
        }

    res = test_client.post("/api/coupons", json={"code": "SALE10"})
    data = res.get_json()

    assert res.status_code == 200
    assert data['total_quantity'] == 2
    assert data['total_price'] == 40000
    assert data['final_price'] == 30000
    assert 'discount_value' in data


def test_remove_coupon(test_client, sample_coupons, mocker):
    class FakeUser:
        is_authenticated = True

    mocker.patch("flask_login.utils._get_user", return_value=FakeUser())

    with test_client.session_transaction() as sess:
        sess['cart'] = {
            '1': {'price': 10000, 'quantity': 1},
            '2': {'price': 20000, 'quantity': 2},
        }
        sess['coupon_slot'] = {'code': 'SALE10'}

    res = test_client.post('/api/coupons', json={'code': 'no'})
    data = res.get_json()

    assert res.status_code == 200
    assert data['discount_value'] == 0
    assert data['final_price'] == data['total_price']


@pytest.mark.parametrize("cart, code ,expected", [
    ({'1': {'price': 10000, 'quantity': 2}}, 'no', {
                                                     'total_price': 20000,
                                                     'discount_value': 0,
                                                     'final_price': 20000,
                                                 }),
    ({'2': {'price': 20000, 'quantity': 2}}, 'SALE10', {
                                                     'total_price': 40000,
                                                     'discount_value': 10000,
                                                     'final_price': 30000,
                                                 }),
    ({'3': {'price': 10000, 'quantity': 2}}, 'SALE15P', {
                                                     'total_price': 20000,
                                                     'discount_value': 3000,
                                                     'final_price': 17000,
                                                 }),
    ({'4': {'price': 10000, 'quantity': 1}}, 'SALE20', {
                                                     'total_price': 10000,
                                                     'discount_value': 20000,
                                                     'final_price': 0,
                                                 }),
], ids=["no_coupon",
        "fixed_coupon",
        "percent_coupon",
        "discount_greater_total"]
)
def test_stats_cart_discount(test_client, sample_coupons, mocker, cart, code, expected):
    class FakeUser:
        is_authenticated = True

    mocker.patch("flask_login.utils._get_user", return_value=FakeUser())

    with test_client.session_transaction() as sess:
        sess['cart'] =cart

    res = test_client.post('/api/coupons', json={'code': code})
    data = res.get_json()

    assert res.status_code == 200
    assert data['total_price'] == expected['total_price']
    assert data['discount_value'] == expected['discount_value']
    assert data['final_price'] == expected['final_price']

    with test_client.session_transaction() as sess:
        if code == 'no':
            assert 'coupon_slot' not in sess
        else:
            assert sess['coupon_slot']['code'] == code

            if code == 'SALE15P':
                assert sess['coupon_slot']['value'] == 15
