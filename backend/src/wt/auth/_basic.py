import os

from wt.auth._manage import authenticate


def basic_auth(username, password, **_):
    # FIXME: @inject doesn't work here. Inject model instead initialize it
    from wt.loader import prepare_db
    from wt.provider.db.models.user import DbUserModel
    db_url = os.environ.get("DB_URL")
    user_model = DbUserModel(prepare_db(db_url))
    user = authenticate(user_model, username, password)
    if user:
        return {"sub": user}
    return None
