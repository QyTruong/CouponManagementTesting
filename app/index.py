import math
from flask import render_template, request, session, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import redirect
from app import app, dao, utils, login
from app.dao.dao_category import load_categories
from app.dao.dao_coupon import count_used_coupons, load_coupons, apply_coupon, load_coupon_by_code
from app.dao.dao_coupon_user import load_coupons_by_user_id
from app.dao.dao_product import load_products, load_product_by_id, count_products
from app.dao.dao_user import add_user, auth_user, get_user_by_id
from app.dao.dao_order import load_orders_by_user_id, add_order, load_order_by_id, pay_order
from app.payment import StripePayment

@app.route('/')
def index():
    kw = request.args.get('kw')
    page = int(request.args.get('page', 1))
    category_id = request.args.get('category_id')

    products = load_products(kw=kw, category_id=category_id, page=page)

    return render_template('index.html', products=products, pages=math.ceil(count_products()/app.config['PAGE_SIZE']))

@app.route('/products/<id>', methods=['GET'])
def product_detail(id):
    product = load_product_by_id(id=id)

    return render_template('product_detail.html', product=product)

@app.context_processor
def common_responses():
    return {
        'categories' : load_categories(),
        'stats_cart' : utils.stats_cart(session.get('cart'), session.get('coupon_slot')),
        'coupons' : load_coupons(),
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

        cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            "quantity": 1,
        }


    session['cart'] = cart

    return jsonify(utils.stats_cart(cart=cart, coupon=session.get('coupon_slot')))


@app.route('/api/cart/<id>', methods=['delete'])
def delete_from_cart(id):
    cart = session.get('cart')

    if cart and id in cart:
        del cart[id]

    session['cart'] = cart

    return jsonify(utils.stats_cart(cart=cart, coupon=session.get('coupon_slot')))


@app.route('/api/cart/<id>', methods=['put'])
def update_cart(id):
    cart = session.get('cart')

    if cart and id in cart:
        quantity = int(request.json.get('quantity'))
        cart[id]['quantity'] = quantity

    session['cart'] = cart

    return jsonify(utils.stats_cart(cart=cart, coupon=session.get('coupon_slot')))

@app.route('/coupons', methods=['get'])
def coupon_view():
    used = [c for c in count_used_coupons()]
    coupons_user = zip(load_coupons_by_user_id(current_user.id), used)

    return render_template('coupon.html', coupons_user=coupons_user)

@app.route('/api/coupons', methods=['post'])
def apply_coupon_to_cart():
    cart = session.get('cart')
    code = request.json.get('code')

    if cart:
        if code == 'no':
            session.pop('coupon_slot', None)

            return jsonify({'status': 200} | utils.stats_cart(cart))
        else:
            coupon = load_coupon_by_code(code=code)

            coupon_slot = {
                'code': code,
                'value': coupon.value,
                'coupon_type': coupon.coupon_type.value,
            }

            session['coupon_slot'] = coupon_slot

            return jsonify({'status': 200} | utils.stats_cart(cart, coupon=coupon_slot))

    return jsonify({'status': 404, 'err_msg': 'Giỏ hàng không tồn tại !!'})


@app.route('/orders', methods=['get'])
def orders_view():
    orders = load_orders_by_user_id(current_user.id)

    return render_template('order_list.html', orders=orders)

@app.route('/api/order', methods=['post'])
def order():
    cart = session.get('cart')
    coupon_slot = session.get('coupon_slot')

    try:
        order = add_order(cart=cart, cart_stats=utils.stats_cart(cart=cart))

        if coupon_slot:
            coupon = load_coupon_by_code(code=coupon_slot['code'])
            apply_coupon(order=order, coupon=coupon)
            del session['coupon_slot']

        del session['cart']

        return jsonify({'status': 200})
    except Exception as e:
        print(e)
        return jsonify({'status': 400, 'err_msg': str(e)})


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
    return get_user_by_id(id)


@app.route('/logout')
def logout_process():
    logout_user()
    return redirect('/login')

@app.route('/clear-session')
def clear_session():
    session.clear()
    return "Session cleared!"


@app.route('/payment/<order_id>', methods=['POST'])
def create_checkout_session(order_id):
    try:
        order = load_order_by_id(id=order_id)

        items = [{
            "price_data": {
                "currency": "vnd",
                "product_data": {
                    "name": f"Order #{order.id}"
                },
                "unit_amount": int(order.final_price)
            },
            "quantity": 1
        }]

        metadata = {
            "order_id": order_id,
            "user_id": order.user.id,
        }

        stripe_payment = StripePayment(items=items)
        checkout_session = stripe_payment.create_payment(metadata=metadata)

    except Exception as e:
        return jsonify({"status": 500, "error": str(e)})

    return jsonify({'status': 303, 'url': checkout_session})


@app.route('/webhook', methods=['POST'])
def webhook_payment():
    stripe_payment = StripePayment(items=None)

    try:
        event = stripe_payment.handel_webhook(request=request)


        if event.type == 'checkout.session.completed':
            s = event.data.object

            order_id = s['metadata']['order_id']

            o = load_order_by_id(id=order_id)

            pay_order(order_id=order_id)

            print("Thành công")

    except Exception as e:
        return jsonify({"status": 400, "error": str(e)})

    return jsonify({'status': 200})

@app.route('/success', methods=['GET'])
def pay_success():
    return render_template('/payment/success_page.html')

@app.route('/cancel', methods=['GET'])
def pay_cancel():
    return render_template('payment/cancel_page.html')

if __name__ == '__main__':
    from app.admin import admin

    app.run(debug=True, port=5000)

    # with app.app_context():
    #     ors = count_used_coupons()
    #
    #     for i in range(0, len(ors)):
    #         print(ors[i])


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
