import hashlib
import pytest
from app.dao.dao_user import auth_user
from app.test.test_base import test_app, test_session, sample_users


@pytest.mark.parametrize('username, password',
    [('user1', 'aaaa1111'), ('user2', 'aaaa2222'), ('user3', 'aaaa3333')]
)
def test_auth_user_success(sample_users, username, password):
    actual_user = auth_user(username=username, password=password)

    assert actual_user is not None
    assert actual_user.username == username

@pytest.mark.parametrize('password',
    ['', 'aaaa2223', 'a'*8, '2222'*8, ''*8, 'b'*20]
)
def test_auth_user_wrong_password(sample_users, password):
    actual_user = auth_user(username='user2', password=password)

    assert actual_user is None

@pytest.mark.parametrize('username',
    ['', 'user33', 'user3.', 'user3 ']
)
def test_auth_user_not_exist(sample_users, username):
    actual_user = auth_user(username=username, password='aaaa3333')

    assert actual_user is None

def test_auth_user_inactive(sample_users):
    with pytest.raises(ValueError):
        auth_user(username=sample_users[3].username, password='aaaa4444')




