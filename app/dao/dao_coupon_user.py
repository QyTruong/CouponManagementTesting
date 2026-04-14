from app.models import CouponUser


def load_coupons_by_user_id(user_id):
    return CouponUser.query.filter(CouponUser.user_id.__eq__(user_id)).all()