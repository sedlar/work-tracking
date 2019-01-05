from sqlalchemy import create_engine

from wt.auth import AuthModel
from wt.provider.db.models.auth import DbAuthModel


def prepare_db(db_url):
    engine = create_engine(
        db_url, isolation_level='SERIALIZABLE'
    )
    return engine


def configure_with_db_url(db_url):
    def configure(binder):
        engine = prepare_db(db_url)
        auth_model = DbAuthModel(engine)
        binder.bind(AuthModel, auth_model)

    return configure
