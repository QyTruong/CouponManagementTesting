from datetime import datetime
from flask import render_template, request
from werkzeug.utils import redirect

from app import app, dao, utils, db
from app.dao import create_coupon, add_user
from app.models import CouponType, UserRole


@app.route('/')
def index():

    return render_template('index.html')

@app.route('/register')
def register_view():
    return render_template('register.html')

@app.route('/register', methods=['post'])
def register_process():
    data = request.form

    password = data.get('password')
    confirm = data.get('confirm')
    if password != confirm:
        return render_template('register.html', err_msg='Mật khẩu không khớp')

    try:
        add_user(name=data.get('name'), username=data.get('username'), password=password, avatar=request.files.get('avatar'))
        return redirect('/')
    except Exception as ex:
        return render_template('register.html', err_msg=str(ex))

if __name__ == '__main__':
    from app.admin import admin

    app.run(debug=True)
    # with app.app_context():
    #     try:
    #         create_coupon({
    #             'code': 'SALE10',
    #             'value': 10000,
    #             'coupon_type': CouponType.FIXED,
    #             'max_quantity': 300,
    #             'expiry_date': datetime(2026, 8, 21, 10, 0, 0),
    #         }, role=UserRole.ADMIN)
    #     except Exception as ex:
    #         print(ex)