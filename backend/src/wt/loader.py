from sqlalchemy import create_engine

from wt.projects import ProjectSerializer, ProjectDeserializer, ProjectsApi
from wt.provider.db import session_maker_factory
from wt.provider.db.models.files import DbFilesModel
from wt.provider.db.models.projects import DbProjectsModel
from wt.provider.db.models.user import DbUserModel
from wt.user import UserModel


def configure_with_engine(engine):
    def configure(binder):
        session_maker = session_maker_factory(engine)
        user_model = DbUserModel(session_maker)
        projects_model = DbProjectsModel(
            session_factory=session_maker,
            files_model=DbFilesModel(
                session_factory=session_maker
            )
        )
        projects_api = ProjectsApi(project_model=projects_model)

        binder.bind(UserModel, user_model)
        binder.bind(ProjectsApi, projects_api)
        binder.bind(ProjectDeserializer, ProjectDeserializer())
        binder.bind(ProjectSerializer, ProjectSerializer())

    return configure


def prepare_db(db_url):
    engine = create_engine(
        db_url, isolation_level='SERIALIZABLE', echo=True
    )
    return engine
