import hashlib
from datetime import datetime, timedelta

import pytest
from flask import Flask
from flask_login import LoginManager

from app import db
from app.index import register_routes
from app.models import Product, Category, User, UserRole, Coupon, CouponType, Order, CouponUser


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config['PAGE_SIZE'] = 2
    app.config['TESTING'] = True
    app.config['LOGIN_DISABLED'] = True
    app.secret_key = "HVHVDIU*(D&V*YDV*&DV(*&DV(*"
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    register_routes(app=app)

    return app


@pytest.fixture()
def test_app():
    app = create_app()

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def test_client(test_app):
    return test_app.test_client()


@pytest.fixture
def test_session(test_app):
    yield db.session
    db.session.rollback()

@pytest.fixture()
def sample_categories(test_session):

    c1 = Category(id=1, name="Áo")
    c2 = Category(id=2, name="Quần")
    c3 = Category(id=3, name="Giày")
    c4 = Category(id=4, name="Phụ kiện")

    test_session.add_all([c1, c2, c3, c4])
    test_session.commit()

    return [c1, c2, c3, c4]

@pytest.fixture
def sample_products(test_session):

    p1 = Product(name='Áo thun', price=20000, category_id=1)
    p2 = Product(name='Áo Hoodie', price=50000, category_id=1)
    p3 = Product(name='Áo sơ mi', price=40000, category_id=1)
    p4 = Product(name='Quần dài', price=30000, category_id=2)
    p5 = Product(name='Quần kaki', price=40000, category_id=2)
    p6 = Product(name='Áo trong category quần', price=20000, category_id=2)
    p7 = Product(name='Váy ngắn', price=20000, category_id=2)
    p8 = Product(name='Giày thể thao ', price=60000, category_id=3)
    p9 = Product(name='Dép', price=30000, category_id=3)
    p10 = Product(name='Mũ', price=20000, category_id=4)
    p11= Product(name='Găng tay', price=20000, category_id=4)

    test_session.add_all([p1,p2,p3,p4,p5,p6,p7,p8,p9, p10, p11])
    test_session.commit()

    return [p1,p2,p3,p4,p5,p6,p7,p8,p9, p10, p11]

@pytest.fixture
def sample_users(test_session):
    user1 = User(name="user1",
                username="user1",
                password=str(hashlib.md5("aaaa1111".strip().encode('utf-8')).hexdigest()),
                active=True,
                user_role=UserRole.USER)
    user2 = User(name="user2",
                username="user2",
                password=str(hashlib.md5("aaaa2222".strip().encode('utf-8')).hexdigest()),
                active=True,
                user_role=UserRole.USER)
    user3 = User(name="user3",
                username="user3",
                password=str(hashlib.md5("aaaa3333".strip().encode('utf-8')).hexdigest()),
                active=True,
                user_role=UserRole.USER)
    user4 = User(name="user4",
                username="user4",
                password=str(hashlib.md5("aaaa4444".strip().encode('utf-8')).hexdigest()),
                active=False,
                user_role=UserRole.USER)
    user5 = User(name="user5",
                 username="user5",
                 password=str(hashlib.md5("aaaa5555".strip().encode('utf-8')).hexdigest()),
                 active=False,
                 user_role=UserRole.USER)

    test_session.add_all([user1, user2, user3, user4, user5])
    test_session.commit()

    return [user1, user2, user3, user4, user5]


@pytest.fixture
def sample_coupons(test_session):
    # Những coupons hợp lệ
    coupon1 = Coupon(
        code="SALE10",
        active=True,
        value=10000,
        coupon_type=CouponType.FIXED,
        expiry_date=datetime.now() + timedelta(days=30)
    )
    coupon2 = Coupon(
        code="SALE20",
        active=True,
        value=20000,
        coupon_type=CouponType.FIXED,
        expiry_date=datetime.now() + timedelta(days=30)
    )
    coupon3 = Coupon(
        code="SALE15P",
        active=True,
        value=15,
        coupon_type=CouponType.VARIABLE,
        expiry_date=datetime.now() + timedelta(days=30)
    )
    coupon4 = Coupon(
        code="SALE40P",
        active=True,
        value=40,
        coupon_type=CouponType.VARIABLE,
        expiry_date=datetime.now() + timedelta(days=30)
    )

    test_session.add_all([coupon1, coupon2, coupon3, coupon4])
    test_session.commit()

    return [coupon1, coupon2, coupon3, coupon4]


@pytest.fixture
def sample_orders(test_session):
    order1 = Order(user_id=1, coupon_id=1, total_price=100000, discount=10000, final_price=90000)
    order2 = Order(user_id=1, coupon_id=1, total_price=200000, discount=10000, final_price=190000)
    order3 = Order(user_id=1, coupon_id=2, total_price=300000, discount=10000, final_price=290000)

    test_session.add_all([order1, order2, order3])
    test_session.commit()

    return [order1, order2, order3]


@pytest.fixture
def sample_coupon_users(test_session):
    coupon_user1 = CouponUser(
        user_id=1,
        coupon_id=1,
        usage_limitation=5
    )
    coupon_user2 = CouponUser(
        user_id=1,
        coupon_id=2,
        usage_limitation=10
    )
    coupon_user3 = CouponUser(
        user_id=1,
        coupon_id=3,
        usage_limitation=0
    )

    test_session.add_all([coupon_user1, coupon_user2, coupon_user3])
    test_session.commit()

    return [coupon_user1, coupon_user2, coupon_user3]


@pytest.fixture
def mock_login(mocker):
    class FakeUser:
        id = 1
        is_authenticated = True

    mocker.patch("flask_login.utils._get_user", return_value=FakeUser())
    # mocker.patch("app.dao.dao_order.current_user", new=FakeUser())
