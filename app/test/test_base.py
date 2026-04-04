from app.models import Product, Category
import pytest
from flask import Flask
from app import  db, dao

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
    db.init_app(app)
    app.config['PAGE_SIZE'] = 3

    return app

@pytest.fixture
def test_app():
    app = create_app()

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def test_session(test_app):
    yield db.session
    db.session.rollback()

# @pytest.fixture()
# def categories_sample(test_session):
#     c1 = Category(name="Áo")
#     c2 = Category(name="Quần")
#     c3 = Category(name="Giày")
#     c4 = Category(name="Phụ kiện")
#
#     test_session.add_all([c1, c2, c3, c4])
#     test_session.commit()
#
#     return c1, c2, c3, c4

@pytest.fixture()
def sample_products(test_session):
    # c1, c2, c3, c4 = categories_sample

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

def test_product_names(sample_products):
    actual_products = dao.load_products(kw='Áo thun')

    assert len(actual_products) == 1