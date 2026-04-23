from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

import pytest
from app.dao.dao_coupon import apply_coupon, calculate_discount_value, validate_usage_limitation, count_used_coupon
from app.models import CouponType, CouponUser
from app.test.test_base import test_app, test_session, sample_coupons, test_client, sample_orders, sample_coupon_users


@pytest.mark.parametrize('coupon_type, value, total_price, expected',
    [(CouponType.FIXED, 70000, 200000, 130000), (CouponType.VARIABLE, 40, 1000000, 600000),
     (CouponType.FIXED, 500000, 490000, 0), (CouponType.FIXED, 500000, 500000, 0)]
)
def test_calculate_discount(coupon_type, value, total_price, expected, mocker):
    mock_order = mocker.Mock(total_price=total_price)
    mock_coupon = mocker.Mock(coupon_type=coupon_type, value=value)

    final_price = calculate_discount_value(mock_order, mock_coupon)

    assert final_price == expected



def test_validate_no_permission(mocker, test_app):
    coupon = MagicMock(id=1)
    fake_user = MagicMock(id=1)

    mocker.patch('app.dao.dao_coupon.current_user', fake_user)

    with test_app.app_context():
        with patch('app.dao.dao_coupon.CouponUser.query') as mock_query:
            mock_query.filter.return_value.first.return_value = None

            with pytest.raises(ValueError):
                validate_usage_limitation(coupon)


def test_validate_exceed_usage(mocker, test_app):
    coupon = MagicMock(id=1)
    fake_user = MagicMock(id=1)
    mocker.patch('app.dao.dao_coupon.current_user', fake_user)

    coupon_user = mocker.Mock(usage_limitation=10)

    with test_app.app_context():
        with patch('app.dao.dao_coupon.CouponUser.query') as mock_query:
            mock_query.filter.return_value.first.return_value = coupon_user

            mocker.patch('app.dao.dao_coupon.count_used_coupon', return_value=(1, 10))

            with pytest.raises(ValueError):
                validate_usage_limitation(coupon)

def test_validate_usage_limitation_success(mocker, test_app):
    coupon = MagicMock(id=1)
    fake_user = MagicMock(id=1)
    mocker.patch('app.dao.dao_coupon.current_user', fake_user)

    coupon_user = mocker.Mock(usage_limitation=10)

    with test_app.app_context():
        with patch('app.dao.dao_coupon.CouponUser.query') as mock_query:
            mock_query.filter.return_value.first.return_value = coupon_user

            mocker.patch('app.dao.dao_coupon.count_used_coupon', return_value=(1, 7))

            validate_usage_limitation(coupon)


@pytest.mark.parametrize('coupon_id, expected',
    [(1, 2), (2, 1), (3, 0)]
)
def test_count_used_coupon(sample_orders, mocker, test_app, coupon_id, expected):
    coupon_id = coupon_id

    c_id, used = count_used_coupon(coupon_id=coupon_id)

    assert c_id == coupon_id
    assert used == expected


def test_apply_coupon_success(mocker):
    order = MagicMock(coupon_id=None)
    coupon = MagicMock(expiry_date=datetime.now() + timedelta(days=1))

    mock_usage_limitation = mocker.patch('app.dao.dao_coupon.validate_usage_limitation')

    mock_calc_discount = mocker.patch('app.dao.dao_coupon.calculate_discount_value', return_value=1000)

    mock_commit = mocker.patch('app.dao.dao_coupon.db.session.commit')

    apply_coupon(order, coupon)

    assert order.final_price == 1000
    assert order.coupon == coupon

    mock_usage_limitation.assert_called_once_with(coupon=coupon)
    mock_calc_discount.assert_called_once_with(order=order, coupon=coupon)
    mock_commit.assert_called_once()


def test_apply_coupon_expired(mocker):
    order = MagicMock(coupon_id=None)
    coupon1 = MagicMock(expiry_date=datetime.now() - timedelta(seconds=1))

    with pytest.raises(ValueError) as e:
        apply_coupon(order, coupon1)

def test_apply_coupon_expiry_boundary(mocker):
    fixed_time = datetime(2027, 1, 1, 0, 0, 0)

    mocker.patch('app.dao.dao_coupon.datetime').now.return_value = fixed_time

    order = MagicMock(coupon_id=None)
    coupon = MagicMock(expiry_date=fixed_time)

    mocker.patch('app.dao.dao_coupon.validate_usage_limitation')
    mocker.patch('app.dao.dao_coupon.calculate_discount_value', return_value=1)
    mocker.patch('app.dao.dao_coupon.db.session.commit')

    apply_coupon(order, coupon)

def test_apply_coupon_order_existed_coupon(mocker):
    order = MagicMock(coupon_id=12)
    coupon = MagicMock(expiry_date=datetime.now())

    with pytest.raises(ValueError) as e:
        apply_coupon(order, coupon)

