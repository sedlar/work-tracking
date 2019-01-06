import os

import transaction

from wt.auth._manage import authenticate
from wt.provider.db import session_maker_factory


def _get_user_model():
    # FIXME: @inject doesn't work here. Inject model instead initialize it
    from wt.loader import prepare_db
    from wt.provider.db.models.user import DbUserModel
    db_url = os.environ.get("DB_URL")
    session_maker = session_maker_factory(prepare_db(db_url))
    return DbUserModel(session_maker)


def basic_auth(username, password, **_):
    user_model = _get_user_model()
    with transaction.manager:
        user = authenticate(user_model, username, password)
    if user:
        return {"sub": user}
    return None
