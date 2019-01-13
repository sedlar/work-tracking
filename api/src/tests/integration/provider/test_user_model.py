from wt.user import BoundUser

USERNAME = "username"
HASHED_PASSWORD = b"password"


def test_user_model(user_model):
    user_model.create_user(username=USERNAME, hashed_password=HASHED_PASSWORD)
    user = user_model.get_user(USERNAME)

    assert isinstance(user, BoundUser)
    assert user.username == USERNAME
    assert user.hashed_password == HASHED_PASSWORD
