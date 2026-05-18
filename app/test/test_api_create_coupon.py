import pytest
from app.admin import CouponView
from app.models import Coupon, CouponType
from app import db
from app.test.test_base import test_app


def test_api_create_coupon_success(test_app, mocker):
    mock_create_coupon = mocker.patch("app.admin.create_coupon", return_value="mock_coupon")

    view = CouponView(Coupon, db.session)
    mock_form = mocker.Mock()
    mock_form.data = {
        'code': 'NEWCODE100',
        'value': 100000,
        'coupon_type': CouponType.FIXED,
        'expiry_date': '2024-12-31'
    }

    res = view.create_model(mock_form)

    assert res == "mock_coupon"
    mock_create_coupon.assert_called_once_with(
        code='NEWCODE100',
        value=100000,
        coupon_type=CouponType.FIXED,
        expiry_date='2024-12-31'
    )


@pytest.mark.parametrize('err_msg', [
    'Thời hạn sử dụng phải sau ngày giờ hiện tại',
    'Thời hạn sử dụng phải lớn hơn ít nhất 1 ngày',
    'Giá trị giảm phải lớn hơn 0',
    'Không được vượt quá 500.000 VND',
    'Mệnh giá này không tồn tại',
    'Phiếu giảm giá với hình thức % không được nhỏ hơn 1%',
    'Phiếu giảm giá với hình thức % không được vượt quá 50%',
    'Mã phiếu giảm này đã tồn tại'
])
def test_api_create_coupon_exceptions(test_app, mocker, err_msg):
    mock_create_coupon = mocker.patch("app.admin.create_coupon", side_effect=ValueError(err_msg))
    mock_flash = mocker.patch("app.admin.flash")

    view = CouponView(Coupon, db.session)
    mock_form = mocker.Mock()
    mock_form.data = {
        'code': 'INVALID',
        'value': 50000,
        'coupon_type': CouponType.FIXED,
        'expiry_date': '2024-12-31'
    }

    res = view.create_model(mock_form)

    assert res is False
    mock_create_coupon.assert_called_once_with(
        code='INVALID',
        value=50000,
        coupon_type=CouponType.FIXED,
        expiry_date='2024-12-31'
    )
    mock_flash.assert_called_once_with(err_msg, "error")


def test_api_create_coupon_integrity_error(test_app, mocker):
    mock_create_coupon = mocker.patch("app.admin.create_coupon", side_effect=Exception("Database error"))
    mock_flash = mocker.patch("app.admin.flash")

    view = CouponView(Coupon, db.session)
    mock_form = mocker.Mock()
    mock_form.data = {
        'code': 'ERRORCODE',
        'value': 50000,
        'coupon_type': CouponType.FIXED,
        'expiry_date': '2024-12-31'
    }

    res = view.create_model(mock_form)

    assert res is False
    mock_create_coupon.assert_called_once_with(
        code='ERRORCODE',
        value=50000,
        coupon_type=CouponType.FIXED,
        expiry_date='2024-12-31'
    )
    mock_flash.assert_called_once_with("Database error", "error")
