from app.models import CouponType


def check_valid_date(current_date, expiration_date):
    return expiration_date >= current_date

def check_valid_percent_value(value, coupon_type):
    if coupon_type == CouponType.VARIABLE and value > 50:
        raise ValueError('Discount value can not exceed 50 percent')


