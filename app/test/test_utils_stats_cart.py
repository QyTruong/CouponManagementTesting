import pytest
from app.test.test_base import test_app, test_session, test_client
from app.utils import stats_cart

def test_stats_cart_without_coupon(test_client):

    with test_client.session_transaction() as sess:
        sess['cart'] = {
            '1': {
                'id': 1,
                'name': 'aaaa',
                'price': 100000,
                'quantity': 1,
            },
            '2': {
                'id': 2,
                'name': 'bbbb',
                'price': 200000,
                'quantity': 2,
            }
        }

        res = stats_cart(sess['cart'])

        assert res['total_quantity'] == 3
        assert res['total_price'] == 500000
        assert res['final_price'] == 500000
        assert res['discount_value'] == 0

def test_stats_cart_with_coupon(test_client):
    with test_client.session_transaction() as sess:
        sess['cart'] = {
            '1': {
                'id': 1,
                'name': 'aaaa',
                'price': 100000,
                'quantity': 1,
            },
            '2': {
                'id': 2,
                'name': 'bbbb',
                'price': 200000,
                'quantity': 2,
            }
        }
        sess['coupon_slot'] = {
            'code': 'SALE20',
            'value': 20000,
            'coupon_type': 1
        }

        res = stats_cart(sess['cart'], sess['coupon_slot'])

        assert res['total_quantity'] == 3
        assert res['total_price'] == 500000
        assert res['final_price'] == 480000
        assert res['discount_value'] == 20000


def test_stats_cart_with_percentage_coupon(test_client):
    with test_client.session_transaction() as sess:
        sess['cart'] = {
            '1': {
                'id': 1,
                'name': 'aaaa',
                'price': 100000,
                'quantity': 1,
            },
            '2': {
                'id': 2,
                'name': 'bbbb',
                'price': 200000,
                'quantity': 2,
            }
        }
        sess['coupon_slot'] = {
            'code': 'SALE10P',
            'value': 10,
            'coupon_type': 2
        }

        res = stats_cart(sess['cart'], sess['coupon_slot'])

        assert res['total_quantity'] == 3
        assert res['total_price'] == 500000
        assert res['final_price'] == 450000
        assert res['discount_value'] == 50000

def test_stats_cart_discount_over_total_price(test_client):
    with test_client.session_transaction() as sess:
        sess['cart'] = {
            '1': {
                'id': 1,
                'name': 'aaaa',
                'price': 100000,
                'quantity': 1,
            },
            '2': {
                'id': 2,
                'name': 'bbbb',
                'price': 200000,
                'quantity': 2,
            }
        }
        sess['coupon_slot'] = {
            'code': 'SALE600',
            'value': 600000,
            'coupon_type': 1
        }

        res = stats_cart(sess['cart'], sess['coupon_slot'])

        assert res['total_quantity'] == 3
        assert res['total_price'] == 500000
        assert res['final_price'] == 0
        assert res['discount_value'] == 600000

def test_stats_cart_with_empty_cart(test_client):
    with test_client.session_transaction() as sess:
        sess['cart'] = {}

    res = stats_cart(sess['cart'])

    assert res['total_quantity'] == 0
    assert res['total_price'] == 0
    assert res['final_price'] == 0
    assert res['discount_value'] == 0