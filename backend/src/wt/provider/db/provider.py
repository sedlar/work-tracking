from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from zope.sqlalchemy import ZopeTransactionExtension


METADATA = MetaData()


def session_maker_factory(engine):
    return scoped_session(
        sessionmaker(
            bind=engine,
            autocommit=False,
            extension=ZopeTransactionExtension())
    )


class DbModel:
    def __init__(self, session_factory):
        self._session_factory = session_factory

    @property
    def _session(self):
        return self._session_factory()
