import pytest
from datetime import datetime, timedelta

from app.dao.dao_coupon import create_coupon
from app.models import Coupon, CouponType, UserRole
from app.test.test_base import test_app, test_session

def test_create_coupon_fixed_success(test_session):
    code = 'FIXED100K'
    value = 100000
    coupon_type = CouponType.FIXED
    expiry_date = datetime.now() + timedelta(days=2)

    create_coupon(code=code, value=value, coupon_type=coupon_type, expiry_date=expiry_date, role=UserRole.ADMIN)
    c = Coupon.query.filter(Coupon.code == code).first()

    assert c is not None
    assert c.code == code
    assert c.value == value
    assert c.coupon_type == coupon_type
    assert c.expiry_date == expiry_date

def test_create_coupon_variable_success(test_session):
    code = 'VAR10PERCENT'
    value = 10
    coupon_type = CouponType.VARIABLE
    expiry_date = datetime.now() + timedelta(days=3)

    create_coupon(code=code, value=value, coupon_type=coupon_type, expiry_date=expiry_date, role=UserRole.ADMIN)
    c = Coupon.query.filter(Coupon.code == code).first()

    assert c is not None
    assert c.code == code
    assert c.value == value
    assert c.coupon_type == coupon_type
    assert c.expiry_date == expiry_date

def test_create_coupon_duplicate_code(test_session):
    code = 'DUPCODE'
    expiry_date = datetime.now() + timedelta(days=2)


    create_coupon(code=code, value=50000, coupon_type=CouponType.FIXED, expiry_date=expiry_date, role=UserRole.ADMIN)


    with pytest.raises(ValueError):
        create_coupon(code=code, value=100000, coupon_type=CouponType.FIXED, expiry_date=expiry_date, role=UserRole.ADMIN)

@pytest.mark.parametrize("days_offset", [
    -1,
    0,
    0.5,
])
def test_create_coupon_invalid_expiry_date(test_session, days_offset):
    code = f'INVEXP{days_offset}'
    expiry_date = datetime.now() + timedelta(days=days_offset)

    with pytest.raises(ValueError):
        create_coupon(code=code, value=50000, coupon_type=CouponType.FIXED, expiry_date=expiry_date, role=UserRole.ADMIN)

@pytest.mark.parametrize("value, coupon_type", [
    (0, CouponType.FIXED),
    (-100, CouponType.FIXED),
    (0, CouponType.VARIABLE),
    (-10, CouponType.VARIABLE),
])
def test_create_coupon_value_less_than_or_equal_zero(test_session, value, coupon_type):
    code = f'INVVAL_{value}_{coupon_type.name}'
    expiry_date = datetime.now() + timedelta(days=2)

    with pytest.raises(ValueError):
        create_coupon(code=code, value=value, coupon_type=coupon_type, expiry_date=expiry_date, role=UserRole.ADMIN)

@pytest.mark.parametrize("value", [
    600000,
    999,
])
def test_create_coupon_fixed_invalid_value(test_session, value):
    code = f'FIXEDINV{value}'
    expiry_date = datetime.now() + timedelta(days=2)

    with pytest.raises(ValueError):
        create_coupon(code=code, value=value, coupon_type=CouponType.FIXED, expiry_date=expiry_date, role=UserRole.ADMIN)

@pytest.mark.parametrize("value", [
    55,
    51,
])
def test_create_coupon_variable_invalid_value(test_session, value):
    code = f'VARINV{value}'
    expiry_date = datetime.now() + timedelta(days=2)

    with pytest.raises(ValueError):
        create_coupon(code=code, value=value, coupon_type=CouponType.VARIABLE, expiry_date=expiry_date, role=UserRole.ADMIN)
