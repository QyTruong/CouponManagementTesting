import pytest
from app.dao.dao_order import add_order
from app.test.test_base import test_app, test_session, test_client, sample_users

def test_add_order_success(sample_users, test_client, mocker):
    mocker.patch("app.dao.dao_order.current_user", new=sample_users[0])

    mock_add = mocker.patch("app.dao.dao_order.db.session.add")
    mock_commit = mocker.patch("app.dao.dao_order.db.session.commit")

    cart = {
        "1": {
            "id": 1,
            "name": "aaaa",
            "price": 100000,
            "quantity": 2
        },
        "2": {
            "id": 2,
            "name": "bbbb",
            "price": 50000,
            "quantity": 1
        }
    }

    cart_stats = {
        "total_quantity": 3,
        "total_price": 250000,
        "discount_value": 20000,
        "final_price": 230000
    }

    order = add_order(cart=cart, cart_stats=cart_stats)

    assert order.total_price == 250000
    assert order.discount == 20000
    assert order.final_price == 230000
    assert mock_add.call_count == 3
    mock_commit.assert_called_once()

def test_api_order_success(test_client, mocker):
    class FakeUser:
        is_authenticated = True

    mocker.patch('flask_login.utils._get_user', return_value=FakeUser())
    mocker.patch('app.index.current_user', return_value=FakeUser())

    mock_order = mocker.Mock(id=1)

    mocker.patch("app.index.utils.stats_cart", return_value={
            "total_price": 100000,
            "discount_value": 10000,
            "final_price": 90000
        }
    )

    mocker.patch(
        "app.index.add_order",
        return_value=mock_order
    )

    mock_coupon = mocker.Mock(id=1)

    mock_load_coupon = mocker.patch("app.index.load_coupon_by_code",return_value=mock_coupon)

    mock_apply_coupon = mocker.patch("app.index.apply_coupon")

    with test_client.session_transaction() as sess:
        sess["cart"] = {
            "1": {
                "id": 1,
                "price": 100000,
                "quantity": 1
            }
        }

        sess["coupon_slot"] = {
            "code": "SALE10"
        }

    response = test_client.post("/api/order")

    data = response.get_json()

    assert data["status"] == 200

    mock_load_coupon.assert_called_once_with(code="SALE10")
    mock_apply_coupon.assert_called_once_with(order=mock_order, coupon=mock_coupon)

