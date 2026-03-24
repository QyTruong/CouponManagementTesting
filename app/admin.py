from flask import flash
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from werkzeug.utils import redirect
from app import app, db
from app.dao import create_coupon
from app.models import UserRole, Coupon


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class CouponView(AdminView):
    def create_model(self, form):
        try:
            return create_coupon(
                code = form.data['code'],
                value = form.data['value'],
                coupon_type= form.data['coupon_type'],
                max_quantity= form.data['max_quantity'],
                expiry_date= form.data['expiry_date'],
                role=UserRole.ADMIN)
        except ValueError as e:
            flash(str(e), "error")
            return False

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')

admin = Admin(app=app, name='Administration')
admin.add_view(CouponView(Coupon, db.session))
admin.add_view(LogoutView(name='Đăng xuất'))