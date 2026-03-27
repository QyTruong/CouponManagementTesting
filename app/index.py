import math
import os
from datetime import datetime

import cloudinary.uploader
from flask import render_template, request, session, jsonify
from flask_login import login_user, logout_user
from werkzeug.utils import redirect

from app import app, dao, utils, db, login
from app.dao import create_coupon, add_user, auth_user, load_products, count_products, load_categories
from app.models import CouponType, UserRole


@app.route('/')
def index():
    kw = request.args.get('kw')
    page = int(request.args.get('page', 1))
    category_id = request.args.get('category_id')

    products = load_products(kw=kw, category_id=category_id,page=page)

    return render_template('index.html', products=products, pages=math.ceil(count_products()/app.config['PAGE_SIZE']))


@app.context_processor
def common_responses():
    return {
        'categories' : load_categories(),
        'stats_cart' : utils.stats_cart(session.get('cart'))
    }


@app.route('/cart')
def cart_view():
    return render_template('cart.html')

@app.route('/api/cart', methods=['post'])
def add_to_cart():
    cart = session.get('cart')

    if not cart:
        cart = {}

    id = str(request.json.get('id'))

    if id in cart:
        cart[id]['quantity'] += 1
    else:
        name = request.json.get('name')
        price = request.json.get('price')
        print(price)
        cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            "quantity": 1
        }


    session['cart'] = cart

    return jsonify(utils.stats_cart(cart))



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
        print(request.files.get('avatar'))
        add_user(name=data.get('name'), username=data.get('username'), password=password,
                 avatar=request.files.get('avatar'))
        return redirect('/login')
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

@app.route('/clear-session')
def clear_session():
    session.clear()
    return "Session cleared!"

if __name__ == '__main__':
    from app.admin import admin

    app.run(debug=True)





    # with app.app_context():
    #     # resp = cloudinary.uploader.upload('default_product.jpg')
    #     # print(resp['secure_url'])
    #     folder_path = "static/images"
    #     files = [f for f in os.listdir(folder_path)
    #              if os.path.isfile(os.path.join(folder_path, f))]
    #     #
    #     # urls = []
    #     # names = []
    #     cnt = 0
    #     for file in files:
    #         cnt+=1
    #
    #     print(cnt)
    #     #
    #     # print(f'{names} : {urls}')
    #
    #     names = ['belt', 'blouse', 'boots', 'coat', 'gloves', 'hat', 'hoodie', 'jacket',
    #              'jean', 'shirt', 'short', 'skirt', 'slippers', 'sneakers', 'sweater', 't-shirt', 'trouser']
    #
    #     urls = ['http://res.cloudinary.com/dufzeox2u/image/upload/v1774417193/ab9yrblhplxg2k8hlyl0.jpg',
    #             'http://res.cloudinary.com/dufzeox2u/image/upload/v1774417194/c2k82sc8uj1co583c8lq.jpg',
    #             'http://res.cloudinary.com/dufzeox2u/image/upload/v1774417194/hvmi6jppuif9qvsod2f5.jpg',
    #             'http://res.cloudinary.com/dufzeox2u/image/upload/v1774417195/wc8kdl2rbem6kglhkpza.jpg',
    #             'http://res.cloudinary.com/dufzeox2u/image/upload/v1774417195/qruamn2otre7d4c2n8lq.jpg',
    #             'http://res.cloudinary.com/dufzeox2u/image/upload/v1774417196/v0o46bo5ix7z5gir22hz.jpg',
    #             'http://res.cloudinary.com/dufzeox2u/image/upload/v1774417197/vx3fayqdfjougevkxn9l.jpg',
    #             'http://res.cloudinary.com/dufzeox2u/image/upload/v1774417197/hjvpwbrsomseljqkgwtw.jpg',
    #             'http://res.cloudinary.com/dufzeox2u/image/upload/v1774417198/c51y5r424znfmwzuqjb5.jpg',
    #             'http://res.cloudinary.com/dufzeox2u/image/upload/v1774417200/uknvg6x4bitpbn6yhjqu.jpg',
    #             'http://res.cloudinary.com/dufzeox2u/image/upload/v1774417201/xwvyuj5mh0daojjsgenh.jpg',
    #             'http://res.cloudinary.com/dufzeox2u/image/upload/v1774417201/tspbc76epx0zpa9lpx6g.jpg',
    #             'http://res.cloudinary.com/dufzeox2u/image/upload/v1774417202/sjehqtlwaesi2coiawbb.jpg',
    #             'http://res.cloudinary.com/dufzeox2u/image/upload/v1774417203/wlg8xl86pfmrsdjdm7ck.jpg',
    #             'http://res.cloudinary.com/dufzeox2u/image/upload/v1774417203/o7kly7657ygoq8fjqunm.jpg',
    #             'http://res.cloudinary.com/dufzeox2u/image/upload/v1774417204/ehzks18q0s2gzsbma7ci.jpg',
    #             'http://res.cloudinary.com/dufzeox2u/image/upload/v1774417204/cindp2mjq1t3ixpw4xxs.jpg']
    #
    #     name_to_url = dict(zip(names, urls))
    #     for name, url in name_to_url.items():
    #         cnt-=1
    #         print(f'{name}: {url}\n')
    #     print(cnt)

'''

['belt', 'blouse', 'boots', 'coat', 'gloves', 'hat', 'hoodie', 'jacket'
, 'jean', 'shirt', 'short', 'skirt', 'slippers', 'sneakers', 'sweater', 't-shirt', 'trouser'] : 
['http://res.cloudinary.com/dufzeox2u/image/upload/v1774417193/ab9yrblhplxg2k8hlyl0.jpg', 
'http://res.cloudinary.com/dufzeox2u/image/upload/v1774417194/c2k82sc8uj1co583c8lq.jpg', 
'http://res.cloudinary.com/dufzeox2u/image/upload/v1774417194/hvmi6jppuif9qvsod2f5.jpg', 
'http://res.cloudinary.com/dufzeox2u/image/upload/v1774417195/wc8kdl2rbem6kglhkpza.jpg', 
'http://res.cloudinary.com/dufzeox2u/image/upload/v1774417195/qruamn2otre7d4c2n8lq.jpg', 
'http://res.cloudinary.com/dufzeox2u/image/upload/v1774417196/v0o46bo5ix7z5gir22hz.jpg', 
'http://res.cloudinary.com/dufzeox2u/image/upload/v1774417197/vx3fayqdfjougevkxn9l.jpg', 
'http://res.cloudinary.com/dufzeox2u/image/upload/v1774417197/hjvpwbrsomseljqkgwtw.jpg', 
'http://res.cloudinary.com/dufzeox2u/image/upload/v1774417198/c51y5r424znfmwzuqjb5.jpg', 
'http://res.cloudinary.com/dufzeox2u/image/upload/v1774417200/uknvg6x4bitpbn6yhjqu.jpg', 
'http://res.cloudinary.com/dufzeox2u/image/upload/v1774417201/xwvyuj5mh0daojjsgenh.jpg', 
'http://res.cloudinary.com/dufzeox2u/image/upload/v1774417201/tspbc76epx0zpa9lpx6g.jpg', 
'http://res.cloudinary.com/dufzeox2u/image/upload/v1774417202/sjehqtlwaesi2coiawbb.jpg', 
'http://res.cloudinary.com/dufzeox2u/image/upload/v1774417203/wlg8xl86pfmrsdjdm7ck.jpg', 
'http://res.cloudinary.com/dufzeox2u/image/upload/v1774417203/o7kly7657ygoq8fjqunm.jpg', 
'http://res.cloudinary.com/dufzeox2u/image/upload/v1774417204/ehzks18q0s2gzsbma7ci.jpg', 
'http://res.cloudinary.com/dufzeox2u/image/upload/v1774417204/cindp2mjq1t3ixpw4xxs.jpg']

'''
