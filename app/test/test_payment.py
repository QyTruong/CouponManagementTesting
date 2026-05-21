import pytest
from app.test.test_base import test_app, test_session, test_client
from app.payment import StripePayment

def test_create_payment(mocker):
    mock_session = mocker.Mock()
    mock_session.url = "http://checkout.stripe.com/testing"

    mocker.patch("stripe.checkout.Session.create", return_value=mock_session)

    payment = StripePayment(items=[
        {
            "price_data": {
                "currency": "vnd",
                "product_data": {
                    "name": "order1",
                },
                "unit_amount": 100000
            },
            "quantity": 5
        }
    ])

    res = payment.create_payment(metadata={"order_id": 1})

    assert res["url"] ==  "http://checkout.stripe.com/testing"


def test_handle_webhook(mocker):

    fake_event = {"type": "checkout.session.completed"}

    mock_construct_event = mocker.patch("stripe.Webhook.construct_event", return_value=fake_event)

    payment = StripePayment(items=None)
    payment.webhook_secret = "secret"

    fake_request = mocker.Mock()
    fake_request.get_data.return_value = "payload"
    fake_request.headers = {
        'Stripe-Signature': 'signature'
    }

    event = payment.handle_webhook(fake_request)

    mock_construct_event.assert_called_once_with("payload", "signature", "secret")
    assert event['type'] == 'checkout.session.completed'

def test_create_checkout_session(test_client, mocker):
    class FakeUser:
        id = 1
        is_authenticated = True

    mocker.patch("flask_login.utils._get_user", return_value=FakeUser())
    mocker.patch('app.index.current_user', return_value=FakeUser())

    mock_order = mocker.Mock(
        id = 10,
        final_price = 100000,
        user = FakeUser(),
    )

    mocker.patch("app.index.load_order_by_id", return_value=mock_order)

    mocker.patch("app.index.StripePayment.create_payment", return_value={
        "url": "http://checkout.stripe.com/testing"
    })

    res = test_client.post("/payment/10")

    data = res.get_json()

    assert data['status'] == 303
    assert data['url'] == 'http://checkout.stripe.com/testing'


def test_webhook_payment(test_client, mocker):

    mock_event = mocker.Mock()
    mock_event.type = "checkout.session.completed"

    mock_event.data.object = {
        "metadata": {
            "order_id": "1"
        }
    }

    mocker.patch("app.index.StripePayment.handle_webhook", return_value=mock_event)

    mock_pay_order = mocker.patch("app.index.pay_order")

    res = test_client.post("/webhook", data="payload", headers={"Stripe-Signature": "signature"})

    data = res.get_json()

    assert res.status_code == 200
    assert data['status'] == "Thành công"

    mock_pay_order.assert_called_once_with(order_id="1")

def test_webhook_missing_order_id(test_client, mocker):
    mock_event = mocker.Mock()
    mock_event.type = "checkout.session.completed"

    mock_event.data.object = {"metadata": {
        "order_id": None
    }}

    mocker.patch("app.index.StripePayment.handle_webhook", return_value=mock_event)

    res = test_client.post("/webhook")

    data = res.get_json()

    assert res.status_code == 400
    assert data['status'] == "Thiếu order_id trong metadata"