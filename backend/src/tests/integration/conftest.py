import os

import transaction
from pytest import fixture
from sqlalchemy import create_engine

from wt.app import create_app, setup_debugger_from_env
from wt.provider.db import METADATA, session_maker_factory
from wt.provider.db.models.files import DbFilesModel
from wt.provider.db.models.projects import DbProjectsModel
from wt.provider.db.models.deliverables import DbDeliverablesModel
from wt.provider.db.models.user import DbUserModel
from wt.provider.db.models.ids import DbIdsCounterModel, DbObjectsTrackerModel
from wt.projects import ProjectsApi
from wt.user import add_user

USERNAME = "username"
PASSWORD = "password"
HASHED_PASSWORD = b"password"


@fixture(scope='session')
def engine():
    return create_engine(
        os.environ.get("DB_URL"), isolation_level="SERIALIZABLE"
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


@fixture(scope="function", autouse=True)
def run_in_transaction():
    transaction.begin()
    yield
    transaction.abort()


@fixture(scope="session")
def app(engine):
    return create_app(engine).app


@fixture(scope="session", autouse=True)
def debugger():
    setup_debugger_from_env()


@fixture(scope="session")
def user_model(session):
    user_model = DbUserModel(session)
    return user_model


@fixture(scope="session")
def files_model(session):
    files_model = DbFilesModel(session)
    return files_model


@fixture(scope="session")
def projects_model(session, files_model):
    return DbProjectsModel(session, files_model)


@fixture(scope="session")
def deliverables_model(session, files_model):
    return DbDeliverablesModel(session)


@fixture(scope="session")
def ids_counter_model(session):
    return DbIdsCounterModel(session)


@fixture(scope="session")
def objects_tracker_model(session):
    return DbObjectsTrackerModel(session)


@fixture(scope="session")
def projects_api(projects_model):
    return ProjectsApi(
        project_model=projects_model,
    )


@fixture(scope="session")
def get_project(projects_api):
    def func(project_id):
        with transaction.manager:
            return projects_api.get_project(project_id)
    return func


@fixture(scope="session")
def put_project(projects_api):
    def func(project):
        with transaction.manager:
            projects_api.put_project(project)
    return func