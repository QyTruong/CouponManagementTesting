import pytest

from app.test.test_base import test_client


def test_api_register_password_mismatch(test_client, mocker):
    mock_add_user = mocker.patch('app.index.add_user')
    
    data = {
        'name': 'Test User',
        'username': 'testuser',
        'password': 'password123',
        'confirm': 'password456'
    }
    
    res = test_client.post('/register', data=data)
    
    assert res.status_code == 200
    assert 'Mật khẩu không khớp' in res.get_data(as_text=True)
    mock_add_user.assert_not_called()


def test_api_register_add_user_exception(test_client, mocker):
    mock_add_user = mocker.patch('app.index.add_user', side_effect=ValueError("Username đã tồn tại"))
    
    data = {
        'name': 'Test User',
        'username': 'testuser',
        'password': 'password123',
        'confirm': 'password123'
    }
    
    res = test_client.post('/register', data=data)
    
    assert res.status_code == 200
    assert 'Username đã tồn tại' in res.get_data(as_text=True)
    mock_add_user.assert_called_once_with(name='Test User', username='testuser', password='password123', avatar=None)


def test_api_register_success(test_client, mocker):
    mock_add_user = mocker.patch('app.index.add_user')
    
    data = {
        'name': 'Test User',
        'username': 'testuser',
        'password': 'password123',
        'confirm': 'password123'
    }
    
    res = test_client.post('/register', data=data)
    
    assert res.status_code == 302
    assert res.location == '/login'
    mock_add_user.assert_called_once_with(name='Test User', username='testuser', password='password123', avatar=None)
