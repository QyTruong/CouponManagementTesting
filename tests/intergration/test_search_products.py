import pytest
from app.dao.dao_product import load_products
from app.test.test_base import test_app, sample_products, test_session


def test_all(sample_products):
    actual_products = load_products()

    assert len(actual_products) == len(sample_products)

def test_zero(sample_products):
    actual_products_kw = load_products(kw='aaaazzzz')
    assert len(actual_products_kw) == 0

    actual_products_page = load_products(page=10)
    assert len(actual_products_page) == 0

    actual_products_cate = load_products(category_id=100)
    assert len(actual_products_cate) == 0


@pytest.mark.parametrize('kw, expected', [
    ("Áo", 4), ("Áo thun", 1), ("Quần", 3), ("Mũ", 1),
    ("Tất", 0)
])
def test_kw(sample_products, kw, expected):
    actual_products = load_products(kw=kw)

    assert len(actual_products) == expected
    assert all(kw.lower() in p.name.lower() for p in actual_products)


@pytest.mark.parametrize('cate, expected', [
    (1, 3), (2, 4), (4,2), (3,2)
])
def test_cate(sample_products, cate, expected):
    actual_products = load_products(category_id=cate)

    assert len(actual_products) == expected
    assert {p.category_id for p in actual_products} == {cate}


@pytest.mark.parametrize('page, expected', [
    (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 1)
])
def test_paging(sample_products, page, expected):
    actual_products = load_products(page=page)
    assert len(actual_products) == expected


@pytest.mark.parametrize("kw, cate, expected", [
    ("Quần", 2, 3), ("Váy ngắn", 2, 1),
    ("Dép", 3, 1), ("Áo", 1, 3), ("Mũ", 1, 0), ("Găng tay", 2, 0)
])
def test_kw_cate_len(sample_products, kw, cate, expected):
    actual_products = load_products(kw=kw, category_id=cate)

    assert len(actual_products) == expected
    assert all(kw.lower() in p.name.lower() for p in actual_products)


def test_kw_cate_name(sample_products):
    actual_products = load_products(kw="Áo", category_id=1)

    assert {p.name for p in actual_products} == {"Áo thun", "Áo Hoodie", "Áo sơ mi"}


@pytest.mark.parametrize("kw, page, expected", [
    ("Áo", 1, 2), ("Áo", 2, 2), ("Quần", 2, 1),
    ("Quần", 1, 2),("Găng tay", 2, 0), ("Áo thun", 1, 1),
    ("Áo thun", 2, 0), ("Dép", 2, 0)
])
def test_kw_paging(sample_products, kw, page, expected):
    actual_products = load_products(kw=kw, page=page)

    assert len(actual_products) == expected
    assert all(kw.lower() in p.name.lower() for p in actual_products)


@pytest.mark.parametrize("cate, page, expected", [
    (1, 1, 2), (1 , 2, 1), (2 ,1 ,2), (2, 2, 2),
     (1, 3 ,0), (2, 3, 0) , (3, 3, 0), (4, 2 ,0)
])
def test_cate_paging(sample_products, cate, page, expected):
    actual_products = load_products(category_id=cate, page=page)

    assert len(actual_products) == expected


@pytest.mark.parametrize('kw, cate, page, expected', [
    ("Áo", 1, 1, 2), ("Áo thun", 1, 1 ,1), ("Quần", 2, 2, 1),
    ("Váy ngắn", 2, 1, 1), ("Giày thể thao",3 ,1 ,1), ("Mũ", 4, 2, 0),
    ("Áo hoodie", 1, 2, 0), ("Quần", 1, 3, 0)
])
def test_kw_cate_paging(sample_products, kw, cate, page, expected):
    actual_products = load_products(kw=kw, category_id=cate, page=page)

    assert len(actual_products) == expected

    for p in actual_products:
        assert kw.lower() in p.name.lower()
        assert p.category_id == cate
        assert p.price > 0


@pytest.mark.parametrize("kw, cate, page, expected", [
    ("", None, None, 11), ("   ", None, None, 0),("zzzz", None, 1, 0),
    (None, 1, 6, 0),("", 1, 6, 0), (None, 1, 6, 0),
    (None, 1, 1, 2),(None, None, 7, 0), ("Áo", 0, 6, 0),
])
def test_boundary(sample_products, kw, cate, page, expected):
    actual_products = load_products(kw=kw, category_id=cate, page=page)

    assert len(actual_products) == expected


@pytest.mark.parametrize("kw, cate, page", [
    (None, None, 0),("Áo", None, 0), (None, 1, 0),
])
def test_invalid_page(kw, cate, page):
    with pytest.raises(ValueError):
        load_products(kw=kw, category_id=cate, page=page)

