from wt.user import add_user
from wt.provider.db.models.user import DbUserModel


def command_add_user(engine, username, password):
    add_user(
        user_model=DbUserModel(engine=engine),
        username=username,
        password=password
    )
