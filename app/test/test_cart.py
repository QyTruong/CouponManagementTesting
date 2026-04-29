from unittest.mock import MagicMock, patch
import pytest
from pytest_mock import mocker

from app.models import CouponType
from app.test.test_base import test_app, test_session, test_client

def test_add_to_cart_success(test_client):
    res = test_client.post("/api/cart", json={
        "id": 1,
        "name": "Áo thun",
        "price": 200000
    })

    assert res.status_code == 200

    data = res.get_json()

    assert data['total_quantity'] == 1
    assert data['total_price'] == 200000

    with test_client.session_transaction() as sess:
        assert "cart" in sess
        assert "1" in sess["cart"]

def test_add_to_cart_increase_quantity(test_client):
    test_client.post("/api/cart", json={
        "id": 1,
        "name": "Quần jeans",
        "price": 200000
    })

    test_client.post("/api/cart", json={
        "id": 2,
        "name": "Áo khoác",
        "price": 150000
    })

    res = test_client.post("/api/cart", json={
        "id": 1,
        "name": "Quần jeans",
        "price": 200000
    })

    assert res.status_code == 200

    data = res.get_json()

    assert data['total_quantity'] == 3
    assert data['total_price'] == 550000

    with test_client.session_transaction() as sess:
        assert len(sess["cart"]) == 2
        assert sess["cart"]["1"]["quantity"] == 2
        assert sess["cart"]["2"]["quantity"] == 1


def test_update_cart_success(test_client):
    with test_client.session_transaction() as sess:
        sess['cart'] = {
            "1": {
                "id": 1,
                "name": "Áo thun",
                "price": 250000,
                "quantity": 3
            }
        }

    res = test_client.put("/api/cart/1", json={
        "quantity": 15,
    })

    data = res.get_json()

    assert data['total_quantity'] == 15
    with test_client.session_transaction() as sess:
        assert len(sess["cart"]) == 1
        assert sess["cart"]["1"]["quantity"] == 15


@pytest.mark.parametrize("quantity",
    [-2, 0]
)
def test_update_cart_with_invalid_quantity(test_client, quantity):
    with test_client.session_transaction() as sess:
        sess['cart'] = {
            "1": {
                "id": 1,
                "name": "Áo thun",
                "price": 250000,
                "quantity": 3
            }
        }

    res = test_client.put("/api/cart/1", json={
        "quantity": quantity,
    })

    data = res.get_json()

    assert data['status'] == 400
    assert data['total_price'] == 750000

    with test_client.session_transaction() as sess:
        assert len(sess["cart"]) == 1
        assert sess["cart"]["1"]["quantity"] == 3


def test_delete_cart_success(test_client):
    with test_client.session_transaction() as sess:
        sess['cart'] = {
            "1": {
                "id": 1,
                "name": "Hoodie",
                "price": 300000,
                "quantity": 3
            },

            "2": {
                "id": 2,
                "name": "Quần jeans",
                "price": 200000,
                "quantity": 10
            }
        }

    res = test_client.delete("/api/cart/2")

    data = res.get_json()

    assert data['total_quantity'] == 3
    assert data['total_price'] == 900000
    with test_client.session_transaction() as sess:
        assert len(sess["cart"]) == 1
        assert "2" not in sess["cart"]


def test_add_to_cart_with_coupon(test_client):
    with test_client.session_transaction() as sess:
        sess['cart'] = {
            "1": {
                "id": 1,
                "name": "Áo thun",
                "price": 250000,
                "quantity": 3
            }
        }

        sess['coupon_slot'] = {
            "code": "SALE10",
            "value": 10000,
            "coupon_type": CouponType.FIXED.value
        }

    res = test_client.post("/api/cart", json={
        "id": 1,
        "name": "Áo thun",
        "price": 250000
    })

    assert res.status_code == 200

    data = res.get_json()

    assert data['total_quantity'] == 4
    assert data['final_price'] == 990000


def test_delete_cart_with_coupon(test_client):
    with test_client.session_transaction() as sess:
        sess['cart'] = {
            "1": {
                "id": 1,
                "name": "Áo thun",
                "price": 250000,
                "quantity": 3
            },

            "2": {
                "id": 2,
                "name": "Quần jeans",
                "price": 300000,
                "quantity": 3
            }
        }

        sess['coupon_slot'] = {
            "code": "SALE10",
            "value": 10000,
            "coupon_type": CouponType.FIXED.value
        }

    res = test_client.delete("/api/cart/2")

    assert res.status_code == 200

    data = res.get_json()

    assert data['total_quantity'] == 3
    assert data['final_price'] == 740000


def test_update_cart_with_coupon(test_client):
    with test_client.session_transaction() as sess:
        sess['cart'] = {
            "1": {
                "id": 1,
                "name": "Áo thun",
                "price": 250000,
                "quantity": 3
            }
        }

        sess['coupon_slot'] = {
            "code": "SALE10",
            "value": 10000,
            "coupon_type": CouponType.FIXED.value
        }

    res = test_client.put("/api/cart/1", json={
        "quantity": 10,
    })

    assert res.status_code == 200

    data = res.get_json()

    assert data['total_quantity'] == 10
    assert data['final_price'] == 2490000


