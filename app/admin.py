from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from app import app, db
from app.models import UserRole



class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class CouponView(AdminView):
    def on_model_change(self, form, model, is_created):
        pass


admin = Admin(app=app, name='Administration')