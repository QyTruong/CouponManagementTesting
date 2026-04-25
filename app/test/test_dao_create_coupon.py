import pytest
from datetime import datetime, timedelta

from app.dao.dao_coupon import create_coupon
from app.models import Coupon, CouponType
from app.test.test_base import test_app, test_session


def test_create_coupon_success(test_session):
    expiry_date = datetime.now() + timedelta(days=5)

    create_coupon(code='FIXED100', value=100000, coupon_type=CouponType.FIXED, expiry_date=expiry_date)
    c1 = Coupon.query.filter(Coupon.code == 'FIXED100').first()

    assert c1 is not None
    assert c1.code == 'FIXED100'
    assert c1.value == 100000
    assert c1.coupon_type == CouponType.FIXED
    assert c1.expiry_date == expiry_date

    create_coupon(code='VAR20', value=20, coupon_type=CouponType.VARIABLE, expiry_date=expiry_date)
    c2 = Coupon.query.filter(Coupon.code == 'VAR20').first()

    assert c2 is not None
    assert c2.code == 'VAR20'
    assert c2.value == 20
    assert c2.coupon_type == CouponType.VARIABLE


def test_invalid_expiration(test_session):
    now = datetime.now()

    with pytest.raises(ValueError):
        create_coupon(code='TEST1', value=10000, coupon_type=CouponType.FIXED, expiry_date=now - timedelta(days=1))
    with pytest.raises(ValueError):
        create_coupon(code='TEST2', value=10000, coupon_type=CouponType.FIXED, expiry_date=now + timedelta(hours=12))


def test_invalid_value(test_session):
    expiry_date = datetime.now() + timedelta(days=2)

    with pytest.raises(ValueError):
        create_coupon(code='TEST1', value=0, coupon_type=CouponType.FIXED, expiry_date=expiry_date)
    with pytest.raises(ValueError):
        create_coupon(code='TEST2', value=-10, coupon_type=CouponType.FIXED, expiry_date=expiry_date)


def test_fixed_invalid(test_session):
    expiry_date = datetime.now() + timedelta(days=2)

    with pytest.raises(ValueError):
        create_coupon(code='TEST1', value=600000, coupon_type=CouponType.FIXED, expiry_date=expiry_date)
    with pytest.raises(ValueError):
        create_coupon(code='TEST2', value=500, coupon_type=CouponType.FIXED, expiry_date=expiry_date)


def test_variable_invalid(test_session):
    expiry_date = datetime.now() + timedelta(days=2)

    with pytest.raises(ValueError):
        create_coupon(code='TEST1', value=0.5, coupon_type=CouponType.VARIABLE, expiry_date=expiry_date)
    with pytest.raises(ValueError):
        create_coupon(code='TEST2', value=60, coupon_type=CouponType.VARIABLE, expiry_date=expiry_date)


def test_existing_code(test_session):
    expiry_date = datetime.now() + timedelta(days=2)
    create_coupon(code='DUP_CODE', value=10000, coupon_type=CouponType.FIXED, expiry_date=expiry_date)

    with pytest.raises(ValueError):
        create_coupon(code='DUP_CODE', value=20000, coupon_type=CouponType.FIXED, expiry_date=expiry_date)
