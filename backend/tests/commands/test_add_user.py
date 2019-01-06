import transaction

from wt.commands.add_user import command_add_user
from wt.user import BoundUser

USERNAME = "user"
PASSWORD = "password"


def test_add_user_command(engine, user_model):
    command_add_user(engine, USERNAME, PASSWORD)

    with transaction.manager:
        user = user_model.get_user(USERNAME)

    assert isinstance(user, BoundUser)
    assert user.username == USERNAME
