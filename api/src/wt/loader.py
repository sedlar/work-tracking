from sqlalchemy import create_engine

from wt.entities.deliverables import DeliverableDeserializer, DeliverableSerializer
from wt.entities.deliverables import DeliverablesApi
from wt.entities.issues import IssueSerializer, IssueDeserializer, IssuesApi
from wt.entities.projects import ProjectSerializer, ProjectDeserializer, ProjectsApi
from wt.fields.files import FileDeserializer, FileSerializer
from wt.fields.links import LinkSerializer, LinkDeserializer
from wt.fields.tags import TagSerializer, TagDeserializer
from wt.fields.tasks import TaskDeserializer, TaskSerializer
from wt.links import EntityLinksApi
from wt.provider.db import session_maker_factory
from wt.provider.db.models.entities import DbProjectsModel, DbDeliverablesModel, DbIssuesModel
from wt.provider.db.models.fields import DbFilesModel, DbLinksModel, DbTagsModel, DbTasksModel
from wt.provider.db.models.ids import DbIdsCounterModel, DbObjectsTrackerModel
from wt.provider.db.models.links import DbEntityLinksModel
from wt.provider.db.models.user import DbUserModel
from wt.user import UserModel


def configure_with_engine(engine):
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
        )
        entity_links_api = EntityLinksApi(
            entity_links_model=entity_links_model,
            objects_tracker_model=objects_tracker_model,
        )
        binder.bind(UserModel, user_model)
        binder.bind(ProjectsApi, projects_api)
        binder.bind(DeliverablesApi, deliverables_api)
        binder.bind(IssuesApi, issues_api)
        binder.bind(EntityLinksApi, entity_links_api)

    def init_serialization(binder):
        file_serializer = FileSerializer()
        link_serializer = LinkSerializer()
        tag_serializer = TagSerializer()
        task_serializer = TaskSerializer()
        project_serializer = ProjectSerializer(file_serializer)
        issue_serializer = IssueSerializer(
            files_serializer=file_serializer,
            links_serializer=link_serializer,
            tags_serializer=tag_serializer,
            tasks_serializer=task_serializer,
        )
        file_deserializer = FileDeserializer()
        link_deserializer = LinkDeserializer()
        tag_deserializer = TagDeserializer()
        task_deserializer = TaskDeserializer()
        project_deserializer = ProjectDeserializer(file_deserializer)
        issue_deserializer = IssueDeserializer(
            files_deserializer=file_deserializer,
            links_deserializer=link_deserializer,
            tags_deserializer=tag_deserializer,
            tasks_deserializer=task_deserializer,
        )
        binder.bind(ProjectDeserializer, project_deserializer)
        binder.bind(ProjectSerializer, project_serializer)
        binder.bind(DeliverableDeserializer, DeliverableDeserializer())
        binder.bind(DeliverableSerializer, DeliverableSerializer())
        binder.bind(IssueSerializer, issue_serializer)
        binder.bind(IssueDeserializer, issue_deserializer)

    return configure


def prepare_db(db_url):
    engine = create_engine(
        db_url, isolation_level='SERIALIZABLE', echo=True
    )
    return engine
