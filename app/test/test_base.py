import hashlib

import pytest
from flask import Flask
from app import db
from app.index import register_routes
from app.models import Product, Category, User, UserRole


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config['PAGE_SIZE'] = 2
    app.config['TESTING'] = True
    app.secret_key = "HVHVDIU*(D&V*YDV*&DV(*&DV(*"
    db.init_app(app)

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

    test_session.add_all([user1, user2, user3, user4])
    test_session.commit()



