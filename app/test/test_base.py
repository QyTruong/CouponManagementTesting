import pytest
from flask import Flask
from app import db
from app.dao.dao_product import load_products
from app.models import Product, Category


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config['PAGE_SIZE'] = 2
    db.init_app(app)

    return app


@pytest.fixture()
def test_app():
    app = create_app()

    with app.app_context():
        db.create_all()
        yield
        db.drop_all()

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
    p3 = Product(name='Quần dài', price=30000, category_id=2)
    p4 = Product(name='Áo trong category quần', price=20000, category_id=2)
    p5 = Product(name='Váy ngắn', price=20000, category_id=2)
    p6 = Product(name='Giày thể thao ', price=60000, category_id=3)
    p7 = Product(name='Dép', price=30000, category_id=3)
    p8 = Product(name='Mũ', price=20000, category_id=4)
    p9 = Product(name='Găng tay', price=20000, category_id=4)
    test_session.add_all([p1,p2,p3,p4,p5,p6,p7,p8,p9])
    test_session.commit()

    return [p1,p2,p3,p4,p5,p6,p7,p8,p9]


def test_all(sample_products):
    actual = load_products()

    assert len(actual) == 6


