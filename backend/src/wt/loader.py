from sqlalchemy import create_engine

from wt.provider.db.models.user import DbUserModel
from wt.provider.db import session_maker_factory
from wt.user import UserModel


def configure_with_engine(engine):
    def configure(binder):
        session_maker = session_maker_factory(engine)
        user_model = DbUserModel(session_maker)
        binder.bind(UserModel, user_model)

    return configure


def prepare_db(db_url):
    engine = create_engine(
        db_url, isolation_level='SERIALIZABLE', echo=True
    )
    return engine
