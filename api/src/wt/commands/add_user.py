import transaction

from wt.provider.db import session_maker_factory
from wt.provider.db.models.user import DbUserModel
from wt.user import add_user


def command_add_user(engine, username, password):
    session_maker = session_maker_factory(engine)
    user_model = DbUserModel(session_maker)

    with transaction.manager:
        add_user(
            user_model=user_model,
            username=username,
            password=password
        )
