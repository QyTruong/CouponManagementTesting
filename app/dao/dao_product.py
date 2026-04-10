from flask import current_app
from app.models import Product


def load_products(kw=None, category_id=None, page=None):
    query = Product.query

    if kw:
        query = query.filter(Product.name.contains(kw))

    if category_id:
        query = query.filter(Product.category_id.__eq__(category_id))

    if page:
        start = (page - 1) * current_app.config['PAGE_SIZE']
        query = query.slice(start, start + current_app.config['PAGE_SIZE'])

    return query.all()

def load_product_by_id(id):
    return Product.query.filter(Product.id.__eq__(id)).first()

def count_products():
    return Product.query.count()