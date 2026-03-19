# ==== Created coupon ====
from app.models import UserRole


def create_coupon(data, role):
    if role is not UserRole.ADMIN:
        raise Exception('Only admin can create coupons')

