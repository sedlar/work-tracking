from copy import deepcopy
from datetime import datetime
from typing import List, Optional

from sqlalchemy import select, delete
from zope.sqlalchemy import mark_changed

from wt.common import Money, Currency
from wt.entities.deliverables import (
    DeliverablesModel,
    BoundDeliverable,
    DeliverableDoesNotExist,
    Deliverable,
    DeliverableStatus,
)
from wt.ids import EntityId
from wt.entities.issues import (
    IssuesModel,
    Issue,
    BoundIssue,
    IssuePriority,
    IssueType,
    IssueStatus,
    IssueDoesNotExist,
)
from wt.entities.projects import ProjectsModel, Project, ProjectStatus, ProjectDoesNotExist
from wt.fields.files import FilesModel
from wt.fields.links import LinksModel
from wt.fields.tags import TagsModel
from wt.fields.tasks import TasksModel
from wt.provider.db import DbModel
from wt.provider.db._utils import insert_or_update
from wt.provider.db.tables import PROJECTS_TABLE, DELIVERABLES_TABLE, ISSUES_TABLE


class DbEntityModel(DbModel):
    _id_column = None
    _table = None
    _does_not_exist_error = Exception

    def _put_entity(self, entity):
        update_data = self._entity_to_dict(entity)
        insert_data = deepcopy(update_data)
        insert_data[self._id_column.name] = self._get_entity_id(entity).full_id
        insert_data["created_on"] = datetime.now()
        self._session.execute(
            insert_or_update(
                self._table,
                insert_data,
                update_data,
                [self._id_column]
            )
        )
        mark_changed(self._session)

    def _get_entity(self, entity_id):
        query = select([self._table]).where(self._id_column == str(entity_id))
        result = self._session.execute(query).fetchone()
        if not result:
            raise self._does_not_exist_error(entity_id)
        return self._row_to_entity(result)

    def _get_entities(self, project_id: Optional[EntityId], offset: int, limit: int):
        query = select([self._table]).offset(offset)
        if project_id:
            query = query.where(self._table.c.project_id == project_id.project_id)
        query = query.limit(limit)
        query = query.order_by(self._id_column)

        result = self._session.execute(query).fetchall()
        return [
            self._row_to_entity(row)
            for row
            in result
        ]

    def _delete_entity(self, entity_id):
        query = delete(self._table).where(self._id_column == str(entity_id))
        result = self._session.execute(query)
        if not result.rowcount:
            raise self._does_not_exist_error(entity_id)
        mark_changed(self._session)

    @staticmethod
    def _get_entity_id(entity):
        raise NotImplementedError()

    @staticmethod
    def _entity_to_dict(entity) -> dict:
        raise NotImplementedError()

    @staticmethod
    def _row_to_entity(row):
        raise NotImplementedError()


class DbProjectsModel(ProjectsModel, DbEntityModel):
    _id_column = PROJECTS_TABLE.c.project_id
    _table = PROJECTS_TABLE
    _does_not_exist_error = ProjectDoesNotExist

    def __init__(self, session_factory, files_model: FilesModel):
        super().__init__(session_factory)
        self._files_model = files_model

    def put_project(self, project: Project):
        self._put_entity(project)
        self._files_model.set_entity_files(project.project_id, project.files)

    def get_project(self, project_id: EntityId):
        project = self._get_entity(project_id)
        project.files = self._files_model.get_entity_files(project_id)
        return project

    def get_projects(self, offset: int, limit: int):
        projects = self._get_entities(project_id=None, offset=offset, limit=limit)
        # TODO: Refactor to load files for all projects in single query
        for project in projects:
            project.files = self._files_model.get_entity_files(project.project_id)
        return projects

    def delete_project(self, project_id: EntityId):
        self._delete_entity(project_id)
        self._files_model.set_entity_files(project_id, [])

    @staticmethod
    def _get_entity_id(entity):
        return entity.project_id

    @staticmethod
    def _entity_to_dict(entity):
        return {
            "name": entity.name,
            "status": entity.status.value,
            "date_opened": entity.date_opened,
            "date_closed": entity.date_closed,
            "deadline": entity.deadline,
            "hour_rate_amount": entity.hour_rate.amount,
            "hour_rate_currency": entity.hour_rate.currency.value,
            "description": entity.description,
            "limitations_and_restrictions": entity.limitations_and_restrictions,
            "goals_and_metrics": entity.goals_and_metrics,
            "primary_color": entity.primary_color,
            "secondary_color": entity.secondary_color,
        }

    @staticmethod
    def _row_to_entity(row) -> Project:
        return Project(
            project_id=EntityId(row["project_id"]),
            name=row["name"],
            status=ProjectStatus(row["status"]),
            date_opened=row["date_opened"],
            date_closed=row["date_closed"],
            deadline=row["deadline"],
            hour_rate=Money(
                amount=row["hour_rate_amount"],
                currency=Currency(row["hour_rate_currency"]),
            ),
            description=row["description"],
            limitations_and_restrictions=row["limitations_and_restrictions"],
            goals_and_metrics=row["goals_and_metrics"],
            primary_color=row["primary_color"],
            secondary_color=row["secondary_color"],
            files=[]
        )


class DbDeliverablesModel(DeliverablesModel, DbEntityModel):
    _id_column = DELIVERABLES_TABLE.c.object_id
    _table = DELIVERABLES_TABLE
    _does_not_exist_error = DeliverableDoesNotExist

    def put_deliverable(self, deliverable: BoundDeliverable):
        self._put_entity(deliverable)

    def delete_deliverable(self, deliverable_id: EntityId):
        self._delete_entity(deliverable_id)

    def get_deliverable(self, deliverable_id: EntityId) -> BoundDeliverable:
        return self._get_entity(deliverable_id)

    def get_deliverables(
            self,
            project_id: EntityId,
            offset: int,
            limit: int
    ) -> List[BoundDeliverable]:
        return self._get_entities(project_id, offset, limit)

    @staticmethod
    def _get_entity_id(entity):
        return entity.object_id

    @staticmethod
    def _entity_to_dict(entity):
        return {
            "project_id": entity.object_id.project_id,
            "name": entity.name,
            "status": entity.status.value,
            "description": entity.description,
            "date_opened": entity.date_opened,
            "date_closed": entity.date_closed,
            "deadline": entity.deadline,
        }

    @staticmethod
    def _row_to_entity(row) -> BoundDeliverable:
        return BoundDeliverable(
            object_id=EntityId(row["object_id"]),
            deliverable=Deliverable(
                name=row["name"],
                status=DeliverableStatus(row["status"]),
                date_opened=row["date_opened"],
                date_closed=row["date_closed"],
                deadline=row["deadline"],
                description=row["description"],
            )
        )


class DbIssuesModel(IssuesModel, DbEntityModel):
    _id_column = ISSUES_TABLE.c.object_id
    _table = ISSUES_TABLE
    _does_not_exist_error = IssueDoesNotExist

    def __init__(
            self,
            session_factory,
            files_model: FilesModel,
            links_model: LinksModel,
            tags_model: TagsModel,
            tasks_model: TasksModel,
    ):
        # pylint: disable=too-many-arguments
        super().__init__(session_factory)
        self._files_model = files_model
        self._links_model = links_model
        self._tags_model = tags_model
        self._tasks_model = tasks_model

    def put_issue(self, issue: BoundIssue):
        self._put_entity(issue)
        self._files_model.set_entity_files(issue.object_id, issue.files)
        self._links_model.set_entity_links(issue.object_id, issue.links)
        self._tags_model.set_entity_tags(issue.object_id, issue.tags)
        self._tasks_model.set_entity_tasks(issue.object_id, issue.tasks)

    def delete_issue(self, issue_id: EntityId):
        self._delete_entity(issue_id)
        self._files_model.set_entity_files(issue_id, [])
        self._links_model.set_entity_links(issue_id, [])
        self._tags_model.set_entity_tags(issue_id, [])
        self._tasks_model.set_entity_tasks(issue_id, [])

    def get_issue(self, issue_id: EntityId) -> BoundIssue:
        issue = self._get_entity(issue_id)
        issue.files = self._files_model.get_entity_files(issue_id)
        issue.links = self._links_model.get_entity_links(issue_id)
        issue.tags = self._tags_model.get_entity_tags(issue_id)
        issue.tasks = self._tasks_model.get_entity_tasks(issue_id)
        return issue

    def get_issues(self, project_id: EntityId, offset: int, limit: int) -> List[BoundIssue]:
        issues = self._get_entities(project_id, offset, limit)
        for issue in issues:
            issue.files = self._files_model.get_entity_files(issue.object_id)
            issue.links = self._links_model.get_entity_links(issue.object_id)
            issue.tags = self._tags_model.get_entity_tags(issue.object_id)
            issue.tasks = self._tasks_model.get_entity_tasks(issue.object_id)
        return issues

    @staticmethod
    def _get_entity_id(entity) -> EntityId:
        return entity.object_id

    @staticmethod
    def _entity_to_dict(entity):
        return {
            "project_id": entity.object_id.project_id,
            "name": entity.name,
            "status": entity.status.value,
            "priority": entity.priority.value,
            "type": entity.type.value,
            "description": entity.description,
            "date_opened": entity.date_opened,
            "date_closed": entity.date_closed,
            "deadline": entity.deadline,
            "external_type": entity.external_type,
            "hour_rate_amount": entity.hour_rate.amount if entity.hour_rate else None,
            "hour_rate_currency": entity.hour_rate.currency.value if entity.hour_rate else None,
            "estimated_duration": entity.estimated_duration
        }

    @staticmethod
    def _row_to_entity(row) -> BoundIssue:
        hour_rate = None
        if row["hour_rate_amount"] and row["hour_rate_currency"]:
            hour_rate = Money(
                amount=row["hour_rate_amount"],
                currency=Currency(row["hour_rate_currency"]),
            )
        return BoundIssue(
            object_id=EntityId(row["object_id"]),
            issue=Issue(
                name=row["name"],
                status=IssueStatus(row["status"]),
                type_=IssueType(row["type"]),
                priority=IssuePriority(row["priority"]),
                date_opened=row["date_opened"],
                date_closed=row["date_closed"],
                deadline=row["deadline"],
                description=row["description"],
                external_type=row["external_type"],
                estimated_duration=row["estimated_duration"],
                hour_rate=hour_rate,
                files=[],
                links=[],
                tags=[],
                tasks=[],
            )
        )
