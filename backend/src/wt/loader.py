from sqlalchemy import create_engine

from wt.user import UserModel
from wt.provider.db.models.user import DbUserModel


def configure_with_engine(engine):
    def configure(binder):
        user_model = DbUserModel(engine)
        binder.bind(UserModel, user_model)

    return configure


def prepare_db(db_url):
    engine = create_engine(
        db_url, isolation_level='SERIALIZABLE'
    )
    return engine
