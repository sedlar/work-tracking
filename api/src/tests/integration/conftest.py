import os

import transaction
from pytest import fixture
from sqlalchemy import create_engine

from wt.app import create_app, setup_debugger_from_env
from wt.costs.expenditures import ExpendituresApi
from wt.costs.timesheets import TimesheetsApi
from wt.entities import EntityManager
from wt.entities.deliverables import DeliverablesApi
from wt.entities.issues import IssuesApi
from wt.entities.projects import ProjectsApi
from wt.links import EntityLinksApi
from wt.provider.db import METADATA, session_maker_factory
from wt.provider.db.models.costs import DbTimesheetsModel, DbExpendituresModel
from wt.provider.db.models.entities import DbProjectsModel, DbDeliverablesModel, DbIssuesModel
from wt.provider.db.models.fields import DbFilesModel, DbLinksModel, DbTagsModel, DbTasksModel
from wt.provider.db.models.ids import DbIdsCounterModel, DbObjectsTrackerModel
from wt.provider.db.models.links import DbEntityLinksModel
from wt.provider.db.models.user import DbUserModel
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
    return DbUserModel(session)


@fixture(scope="session")
def files_model(session):
    return DbFilesModel(session)


@fixture(scope="session")
def links_model(session):
    return DbLinksModel(session)


@fixture(scope="session")
def tags_model(session):
    return DbTagsModel(session)


@fixture(scope="session")
def tasks_model(session):
    return DbTasksModel(session)


@fixture(scope="session")
def projects_model(session, files_model):
    return DbProjectsModel(session, files_model)


@fixture(scope="session")
def deliverables_model(session, files_model):
    return DbDeliverablesModel(session)


@fixture(scope="session")
def issues_model(session, files_model, links_model, tags_model, tasks_model):
    return DbIssuesModel(
        session,
        files_model=files_model,
        links_model=links_model,
        tags_model=tags_model,
        tasks_model=tasks_model,
    )


@fixture(scope="session")
def ids_counter_model(session):
    return DbIdsCounterModel(session)


@fixture(scope="session")
def objects_tracker_model(session):
    return DbObjectsTrackerModel(session)


@fixture(scope="session")
def entity_links_model(session):
    return DbEntityLinksModel(session)


@fixture(scope="session")
def timesheets_model(session):
    return DbTimesheetsModel(session)


@fixture(scope="session")
def expenditures_model(session, files_model):
    return DbExpendituresModel(session, files_model)


@fixture(scope="session")
def entity_manager(ids_counter_model, objects_tracker_model):
    return EntityManager(
        ids_counter_model=ids_counter_model,
        objects_tracker_model=objects_tracker_model,
    )


@fixture(scope="session")
def projects_api(projects_model, ids_counter_model, objects_tracker_model):
    return ProjectsApi(
        project_model=projects_model,
        ids_counter_model=ids_counter_model,
        objects_tracker_model=objects_tracker_model
    )


@fixture(scope="session")
def deliverables_api(
        deliverables_model,
        entity_manager,
        entity_links_model
):
    return DeliverablesApi(
        deliverables_model=deliverables_model,
        entity_manager=entity_manager,
        entity_links_model=entity_links_model,
    )


@fixture(scope="session")
def issues_api(
        issues_model,
        entity_manager,
        entity_links_model,
        timesheets_model,
        expenditures_model
):
    return IssuesApi(
        issues_model=issues_model,
        entity_manager=entity_manager,
        entity_links_model=entity_links_model,
        timesheets_model=timesheets_model,
        expenditures_model=expenditures_model,
    )


@fixture(scope="session")
def links_api(entity_links_model, objects_tracker_model):
    return EntityLinksApi(
        entity_links_model=entity_links_model,
        objects_tracker_model=objects_tracker_model,
    )


@fixture(scope="session")
def timesheets_api(objects_tracker_model, timesheets_model):
    return TimesheetsApi(
        objects_tracker_model=objects_tracker_model,
        timesheets_model=timesheets_model,
    )


@fixture(scope="session")
def expenditures_api(objects_tracker_model, expenditures_model):
    return ExpendituresApi(
        objects_tracker_model=objects_tracker_model,
        expenditures_model=expenditures_model,
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


@fixture(scope="session")
def get_deliverable(deliverables_api):
    def func(deliverable_id):
        with transaction.manager:
            return deliverables_api.get_deliverable(deliverable_id)
    return func


@fixture(scope="session")
def post_deliverable(deliverables_api):
    def func(project_id, deliverable):
        with transaction.manager:
            return deliverables_api.create_deliverable(project_id, deliverable)
    return func


@fixture(scope="session")
def get_issue(issues_api):
    def func(issue_id):
        with transaction.manager:
            return issues_api.get_issue(issue_id)
    return func


@fixture(scope="session")
def post_issue(issues_api):
    def func(project_id, issue):
        with transaction.manager:
            return issues_api.create_issue(project_id, issue)
    return func


@fixture(scope="session")
def put_link(links_api):
    def func(entity_id, other_entity_id):
        with transaction.manager:
            return links_api.create_link(entity_id, other_entity_id)
    return func


@fixture(scope="session")
def post_timesheet(timesheets_api):
    def func(object_id, timesheet):
        with transaction.manager:
            return timesheets_api.create_timesheet(object_id, timesheet)
    return func


@fixture(scope="session")
def get_timesheets(timesheets_api):
    def func(object_id, offset=0, limit=1):
        with transaction.manager:
            return timesheets_api.get_timesheets(object_id, offset, limit)
    return func


@fixture(scope="session")
def post_expenditure(expenditures_api):
    def func(object_id, timesheet):
        with transaction.manager:
            return expenditures_api.create_expenditure(object_id, timesheet)
    return func


@fixture(scope="session")
def get_expenditures(expenditures_api):
    def func(object_id, offset=0, limit=1):
        with transaction.manager:
            return expenditures_api.get_expenditures(object_id, offset, limit)
    return func
