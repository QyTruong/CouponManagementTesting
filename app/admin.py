from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from app import app, db
from app.dao import create_coupon
from app.models import UserRole, Coupon


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class CouponView(AdminView):
    def on_model_change(self, form, model, is_created):
        create_coupon({
            'code': model.code,
            'value': model.value,
            'coupon_type': model.coupon_type,
            'max_quantity': model.availability_count,
            'expiry_date': model.expiry_date,
        }, role=UserRole.ADMIN)



admin = Admin(app=app, name='Administration')
admin.add_view(CouponView(Coupon, db.session))