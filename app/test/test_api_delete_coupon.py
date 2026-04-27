import pytest
from app.admin import CouponView
from app.models import Coupon
from app import db
from app.test.test_base import test_app


def test_api_delete_coupon_success(test_app, mocker):
    mock_delete_coupon = mocker.patch("app.admin.delete_coupon")

    view = CouponView(Coupon, db.session)
    mock_model = mocker.Mock()

    res = view.delete_model(mock_model)

    assert res is True
    mock_delete_coupon.assert_called_once_with(coupon=mock_model)


def test_api_delete_coupon_exception(test_app, mocker):
    err_msg = "Không thể xóa mã giảm giá này, vì vẫn đang tồn tại đơn hàng đang xử lý"
    mock_delete_coupon = mocker.patch("app.admin.delete_coupon", side_effect=ValueError(err_msg))
    mock_flash = mocker.patch("app.admin.flash")

    view = CouponView(Coupon, db.session)
    mock_model = mocker.Mock()

    res = view.delete_model(mock_model)

    assert res is False
    mock_delete_coupon.assert_called_once_with(coupon=mock_model)
    mock_flash.assert_called_once_with(err_msg, "error")


def test_api_delete_coupon_database_exception(test_app, mocker):
    err_msg = "Database error"
    mock_delete_coupon = mocker.patch("app.admin.delete_coupon", side_effect=Exception(err_msg))
    mock_flash = mocker.patch("app.admin.flash")

    view = CouponView(Coupon, db.session)
    mock_model = mocker.Mock()

    res = view.delete_model(mock_model)

    assert res is False
    mock_delete_coupon.assert_called_once_with(coupon=mock_model)
    mock_flash.assert_called_once_with(err_msg, "error")
