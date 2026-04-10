from app.models import Category

def load_categories():
    query = Category.query
    return query.all()