from unittest.mock import MagicMock, patch
import pytest
from app.dao.dao_user import auth_user
from app.test.test_base import test_app, test_session, sample_users, test_client


@pytest.mark.parametrize('username, password',
    [('user1', 'aaaa1111'), ('user2', 'aaaa2222'), ('user3', 'aaaa3333')]
)
def test_auth_user_success(sample_users, username, password):
    actual_user = auth_user(username=username, password=password)

    assert actual_user is not None
    assert actual_user.username == username

@pytest.mark.parametrize('password',
    ['', 'aaaa2223', 'wrong', None]
)
def test_auth_user_wrong_password(sample_users, password):
    actual_user = auth_user(username='user2', password=password)

    assert actual_user is None

@pytest.mark.parametrize('username',
    ['', 'user33', 'user3.', 'user3 ', None]
)
def test_auth_user_not_exist(sample_users, username):
    actual_user = auth_user(username=username, password='aaaa3333')

    assert actual_user is None

def test_auth_user_inactive(sample_users):
    with pytest.raises(ValueError):
        auth_user(username=sample_users[3].username, password='aaaa4444')

    with pytest.raises(ValueError):
        auth_user(username=sample_users[4].username, password='aaaa5555')

@pytest.mark.parametrize('username, password',
    [("user1", "aaaa1111"), ("user2", "aaaa2222"), ("user3", "aaaa3333")]
)
def test_login_success(sample_users, test_client, mocker, username, password):
    fake_user = mocker.Mock()

    mock_user = mocker.patch("app.index.auth_user", return_value=fake_user)
    mock_login = mocker.patch("app.index.login_user")

    test_client.post("/login", data={
        "username": username,
        "password": password
    }, content_type="application/x-www-form-urlencoded")

    mock_user.assert_called_once_with(username=username, password=password)
    mock_login.assert_called_once_with(user=fake_user)



def test_login_wrong_info(sample_users, test_client, mocker):
    mocker.patch("app.index.auth_user", return_value=None)
    mock_login = mocker.patch("app.index.login_user")

    test_client.post("/login", data={
        "username": "aaaa",
        "password": "aaaa"
    }, content_type="application/x-www-form-urlencoded")

    mock_login.assert_not_called()


def test_login_miss_info(sample_users, test_client, mocker):
    mocker.patch("app.index.auth_user", return_value=None)
    mock_login = mocker.patch("app.index.login_user")

    test_client.post("/login", data={},
        content_type="application/x-www-form-urlencoded"
    )

    mock_login.assert_not_called()

def test_login_inactive_user(sample_users, test_client, mocker):
    mock_user = mocker.patch("app.index.auth_user", side_effect=ValueError("Tài khoản này bị khóa, không đăng nhập được"))
    mock_login = mocker.patch("app.index.login_user")
    mock_render = mocker.patch("app.index.render_template", return_value="ok")

    test_client.post("/login", data={
        "username": "user4",
        "password": "aaaa4444"
    }, content_type="application/x-www-form-urlencoded")

    mock_render.assert_called_once()
    mock_user.assert_called_once_with(username="user4", password="aaaa4444")
    mock_login.assert_not_called()


def test_login_redirect_next(test_client, mocker):
    fake_user = mocker.Mock()

    mocker.patch("app.index.auth_user", return_value=fake_user)
    mocker.patch("app.index.login_user")

    res = test_client.post("/login?next=/cart", data={
        "username": "user1",
        "password": "aaaa1111"
    })

    assert res.headers["Location"] == "/cart"