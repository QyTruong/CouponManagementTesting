from datetime import datetime
from flask import render_template, request
from flask_login import login_user, logout_user
from werkzeug.utils import redirect

from app import app, dao, utils, db, login
from app.dao import create_coupon, add_user, auth_user
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


@app.route('/login')
def login_view():
    return render_template('login.html')

@app.route('/login', methods=['post'])
def login_process():
    username = request.form.get('username')
    password = request.form.get('password')

    user = auth_user(username=username, password=password)

    if user:
        login_user(user=user)

    next = request.args.get('next')
    return redirect(next if next else '/')

@login.user_loader
def load_user(id):
    return dao.get_user_by_id(id)


@app.route('/logout')
def logout_process():
    logout_user()
    return redirect('/login')



if __name__ == '__main__':
    from app.admin import admin

    app.run(debug=True)
