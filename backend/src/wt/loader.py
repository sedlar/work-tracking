from sqlalchemy import create_engine

from wt.entities.projects import ProjectSerializer, ProjectDeserializer, ProjectsApi
from wt.provider.db import session_maker_factory
from wt.provider.db.models.fields import DbFilesModel
from wt.provider.db.models.projects import DbProjectsModel
from wt.provider.db.models.user import DbUserModel
from wt.provider.db.models.ids import DbIdsCounterModel, DbObjectsTrackerModel
from wt.provider.db.models.deliverables import DbDeliverablesModel
from wt.entities.deliverables import DeliverablesApi
from wt.user import UserModel
from wt.entities.deliverables import DeliverableDeserializer, DeliverableSerializer


def configure_with_engine(engine):
    def configure(binder):
        session_maker = session_maker_factory(engine)
        user_model = DbUserModel(session_maker)
        projects_model = DbProjectsModel(
            session_factory=session_maker,
            files_model=DbFilesModel(
                session_factory=session_maker
            ),
        )
        ids_counter_model = DbIdsCounterModel(session_factory=session_maker)
        deliverables_model = DbDeliverablesModel(session_factory=session_maker)
        objects_tracker_model = DbObjectsTrackerModel(session_factory=session_maker)

        projects_api = ProjectsApi(
            project_model=projects_model,
            ids_counter_model=ids_counter_model,
            objects_tracker_model=objects_tracker_model,
        )
        deliverables_api = DeliverablesApi(
            deliverables_model=deliverables_model,
            ids_counter_model=ids_counter_model,
            objects_tracker_model=objects_tracker_model,
        )

        binder.bind(UserModel, user_model)
        binder.bind(ProjectsApi, projects_api)
        binder.bind(DeliverablesApi, deliverables_api)
        binder.bind(ProjectDeserializer, ProjectDeserializer())
        binder.bind(ProjectSerializer, ProjectSerializer())
        binder.bind(DeliverableDeserializer, DeliverableDeserializer())
        binder.bind(DeliverableSerializer, DeliverableSerializer())

    return configure


def prepare_db(db_url):
    engine = create_engine(
        db_url, isolation_level='SERIALIZABLE', echo=True
    )
    return engine
