import pytest
import hashlib

from app.dao import add_user
from app.models import User
from app.test.test_base import test_app, test_session



@pytest.fixture
def mock_cloudinary(monkeypatch):
    def fake_upload(file):
        return {'secure_url': 'https://fake-image.png'}

    monkeypatch.setattr('cloudinary.uploader.upload', fake_upload)

def test_register_success(test_session):
    add_user(name='test', username='test', password='Test@123', avatar=None)
    u = User.query.filter(User.username == 'test').first()

    assert u is not None
    assert u.name == 'test'
    assert u.username == 'test'
    assert u.password == hashlib.md5('Test@123'.encode('utf-8')).hexdigest()


@pytest.mark.parametrize('password', [
    '1', '1'*8, 'a'*8, '!@!'*2
])
def test_invalid_password(password, test_session):
    with pytest.raises(ValueError):
        add_user(name='abc', username='demodemo', password=password, avatar=None)


def test_existing_username(test_session):
    add_user(name='abc', username='demodemo', password='123ABC1231', avatar=None)

    with pytest.raises(ValueError):
        add_user(name='abc', username='demodemo', password='123ABC1231', avatar=None)


def test_avatar(test_session, mock_cloudinary):
    add_user(name='abc', username='demodemo', password='123ABC1231', avatar="aaaa")

    u = User.query.filter(User.username.__eq__('demodemo')).first()

    assert u is not None
    assert u.name == 'abc'
    assert u.password == str(hashlib.md5('123ABC1231'.encode('utf-8')).hexdigest())
    assert u.avatar == 'https://fake-image.png'


