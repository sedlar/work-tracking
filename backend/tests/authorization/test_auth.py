from pytest import mark
from wt.user import BoundUser
from wt.auth import basic_auth


USERNAME = "username"
PASSWORD = "password"


@mark.usefixtures("user")
def test_auth_success():
    authentication = basic_auth(username=USERNAME, password=PASSWORD)
    assert isinstance(authentication, dict)
    user = authentication.get("sub")
    assert isinstance(user, BoundUser)
    assert user.username == USERNAME


def test_auth_bad_password():
    assert not basic_auth(username=USERNAME, password="BAD_PASSWORD")


def test_auth_unknown_user():
    assert not basic_auth(username="unknown_user", password=PASSWORD)
