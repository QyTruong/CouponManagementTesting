from flask import flash
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from werkzeug.utils import redirect
from app import app, db
from app.dao import create_coupon
from app.models import UserRole, Coupon, Product, Category, User


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class UserView(AdminView):
    column_list = ['id', 'name', 'username', 'user_role', 'active', 'joined_date']
    column_searchable_list = ['name']
    column_filters = ['name']
    column_exclude_list = ['password', 'avatar']

class ProductView(AdminView):
   column_list = ['id', 'name', 'price', 'category']
   column_filters = ['name', 'price', 'category']
   column_searchable_list = ['name']
   column_sortable_list = ['price']
   can_export = True
   edit_modal = True

class CategoryView(AdminView):
    column_list = ['id', 'name']
    column_filters = ['name']
    column_searchable_list = ['name']

class CouponView(AdminView):
    column_list = ['id', 'code', 'coupon_type', 'value', 'max_quantity','created_at', 'expiry_date']
    column_filters = ['code', 'created_at', 'expiry_date']
    column_searchable_list = ['code', 'created_at', 'expiry_date']
    column_sortable_list = ['value', 'expiry_date']
    can_export = True
    edit_modal = True
    page_size = 10


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
admin.add_view(ProductView(Product, db.session))
admin.add_view(CategoryView(Category, db.session))
admin.add_view(UserView(User, db.session))
admin.add_view(LogoutView(name='Đăng xuất'))