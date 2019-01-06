import os

import transaction
from pytest import fixture
from sqlalchemy import create_engine

from wt.app import create_app, setup_debugger_from_env
from wt.provider.db import METADATA, session_maker_factory
from wt.provider.db.models.user import DbUserModel
from wt.user import add_user

USERNAME = "username"
PASSWORD = "password"
HASHED_PASSWORD = b"password"


@fixture(scope='session')
def engine():
    return create_engine(
        os.environ.get("DB_URL"), echo=True
    )


@fixture(scope='session')
def session(engine):
    return session_maker_factory(engine)


@fixture
def user(user_model):
    with transaction.manager:
        return add_user(user_model=user_model, username=USERNAME, password=PASSWORD)


@fixture(scope="function", autouse=True)
def init_db(engine):
    METADATA.drop_all(engine)
    METADATA.create_all(engine)


@fixture(scope="session")
def app(engine):
    return create_app(engine)


@fixture(scope="session", autouse=True)
def debugger():
    setup_debugger_from_env()


@fixture(scope="session")
def user_model(session):
    user_model = DbUserModel(session)
    return user_model
