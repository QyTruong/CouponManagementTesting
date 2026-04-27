import pytest
from app.dao.dao_coupon import delete_coupon
from app.models import Coupon
from app.test.test_base import test_app, test_session, sample_users, sample_coupons, sample_orders


def test_delete_coupon_success(test_session, sample_users, sample_coupons, sample_orders):
    coupon_to_delete = sample_coupons[2]

    delete_coupon(coupon_to_delete)

    deleted_coupon = Coupon.query.filter(Coupon.id == coupon_to_delete.id).first()

    assert deleted_coupon is not None
    assert deleted_coupon.active is False


def test_delete_coupon_processing_order(test_session, sample_users, sample_coupons, sample_orders):
    coupon_to_delete = sample_coupons[0]

    with pytest.raises(ValueError):
        delete_coupon(coupon_to_delete)

    not_deleted_coupon = Coupon.query.filter(Coupon.id == coupon_to_delete.id).first()

    assert not_deleted_coupon.active is True
