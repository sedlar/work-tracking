from sqlalchemy import create_engine

from wt.provider.db.models.auth import DbAuthModel
from wt.provider.db.models.projects import DbProjectModel


def prepare_db(db_url):
    engine = create_engine(
        db_url, isolation_level='SERIALIZABLE'
    )
    return engine


def load_components(db_url):
    engine = prepare_db(db_url)

    DbProjectModel()
    DbAuthModel()
