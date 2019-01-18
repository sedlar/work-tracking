from sqlalchemy import create_engine

from wt.costs.expenditures import (
    ExpendituresSerializer,
    ExpendituresDeserializer,
    ExpendituresApi,
)
from wt.costs.timesheets import (
    TimesheetsSerializer,
    TimesheetsDeserializer,
    TimesheetsApi,
)
from wt.entities.deliverables import DeliverableDeserializer, DeliverableSerializer, DeliverablesApi
from wt.entities.issues import IssuesSerializer, IssuesDeserializer, IssuesApi
from wt.entities.projects import ProjectsSerializer, ProjectsDeserializer, ProjectsApi
from wt.fields.files import FilesDeserializer, FilesSerializer
from wt.fields.links import LinkSerializer, LinksDeserializer
from wt.fields.tags import TagsSerializer, TagsDeserializer
from wt.fields.tasks import TasksDeserializer, TasksSerializer
from wt.links import EntityLinksApi
from wt.provider.db import session_maker_factory
from wt.provider.db.models.costs import DbTimesheetsModel, DbExpendituresModel
from wt.provider.db.models.entities import DbProjectsModel, DbDeliverablesModel, DbIssuesModel
from wt.provider.db.models.fields import DbFilesModel, DbLinksModel, DbTagsModel, DbTasksModel
from wt.provider.db.models.ids import DbIdsCounterModel, DbObjectsTrackerModel
from wt.provider.db.models.links import DbEntityLinksModel
from wt.provider.db.models.user import DbUserModel
from wt.user import UserModel


def configure_with_engine(engine):
    # pylint: disable=too-many-statements
    def configure(binder):
        init_apis(binder)
        init_serialization(binder)

    def init_apis(binder):
        # pylint: disable=too-many-locals
        session_maker = session_maker_factory(engine)
        user_model = DbUserModel(session_maker)
        files_model = DbFilesModel(session_factory=session_maker)
        links_model = DbLinksModel(session_factory=session_maker)
        tags_model = DbTagsModel(session_factory=session_maker)
        tasks_model = DbTasksModel(session_factory=session_maker)
        projects_model = DbProjectsModel(
            session_factory=session_maker,
            files_model=files_model,
        )
        ids_counter_model = DbIdsCounterModel(session_factory=session_maker)
        deliverables_model = DbDeliverablesModel(session_factory=session_maker)
        timesheets_model = DbTimesheetsModel(session_factory=session_maker)
        expenditures_model = DbExpendituresModel(
            session_factory=session_maker,
            files_model=files_model,
        )
        issues_model = DbIssuesModel(
            session_factory=session_maker,
            files_model=files_model,
            links_model=links_model,
            tags_model=tags_model,
            tasks_model=tasks_model,
        )
        objects_tracker_model = DbObjectsTrackerModel(session_factory=session_maker)
        entity_links_model = DbEntityLinksModel(session_factory=session_maker)
        projects_api = ProjectsApi(
            project_model=projects_model,
            ids_counter_model=ids_counter_model,
            objects_tracker_model=objects_tracker_model,
        )
        deliverables_api = DeliverablesApi(
            deliverables_model=deliverables_model,
            ids_counter_model=ids_counter_model,
            objects_tracker_model=objects_tracker_model,
            entity_links_model=entity_links_model,
        )
        issues_api = IssuesApi(
            issues_model=issues_model,
            ids_counter_model=ids_counter_model,
            objects_tracker_model=objects_tracker_model,
            entity_links_model=entity_links_model,
            timesheets_model=timesheets_model,
            expenditures_model=expenditures_model,
        )
        entity_links_api = EntityLinksApi(
            entity_links_model=entity_links_model,
            objects_tracker_model=objects_tracker_model,
        )
        timesheets_api = TimesheetsApi(
            objects_tracker_model=objects_tracker_model,
            timesheets_model=timesheets_model,
        )
        expenditures_api = ExpendituresApi(
            objects_tracker_model=objects_tracker_model,
            expenditures_model=expenditures_model,
        )
        binder.bind(UserModel, user_model)
        binder.bind(ProjectsApi, projects_api)
        binder.bind(DeliverablesApi, deliverables_api)
        binder.bind(IssuesApi, issues_api)
        binder.bind(EntityLinksApi, entity_links_api)
        binder.bind(TimesheetsApi, timesheets_api)
        binder.bind(ExpendituresApi, expenditures_api)

    def init_serialization(binder):
        files_serializer = FilesSerializer()
        links_serializer = LinkSerializer()
        tags_serializer = TagsSerializer()
        tasks_serializer = TasksSerializer()
        projects_serializer = ProjectsSerializer(files_serializer)
        issues_serializer = IssuesSerializer(
            files_serializer=files_serializer,
            links_serializer=links_serializer,
            tags_serializer=tags_serializer,
            tasks_serializer=tasks_serializer,
        )
        files_deserializer = FilesDeserializer()
        links_deserializer = LinksDeserializer()
        tags_deserializer = TagsDeserializer()
        tasks_deserializer = TasksDeserializer()
        projects_deserializer = ProjectsDeserializer(files_deserializer)
        issue_deserializer = IssuesDeserializer(
            files_deserializer=files_deserializer,
            links_deserializer=links_deserializer,
            tags_deserializer=tags_deserializer,
            tasks_deserializer=tasks_deserializer,
        )
        expenditures_serializer = ExpendituresSerializer(
            files_serializer=files_serializer
        )
        expenditures_deserializer = ExpendituresDeserializer(
            files_deserializer=files_deserializer
        )
        binder.bind(ProjectsDeserializer, projects_deserializer)
        binder.bind(ProjectsSerializer, projects_serializer)
        binder.bind(DeliverableDeserializer, DeliverableDeserializer())
        binder.bind(DeliverableSerializer, DeliverableSerializer())
        binder.bind(IssuesSerializer, issues_serializer)
        binder.bind(IssuesDeserializer, issue_deserializer)
        binder.bind(TimesheetsSerializer, TimesheetsSerializer())
        binder.bind(TimesheetsDeserializer, TimesheetsDeserializer())
        binder.bind(ExpendituresSerializer, expenditures_serializer)
        binder.bind(ExpendituresDeserializer, expenditures_deserializer)

    return configure


def prepare_db(db_url):
    engine = create_engine(
        db_url, isolation_level='SERIALIZABLE', echo=True
    )
    return engine
