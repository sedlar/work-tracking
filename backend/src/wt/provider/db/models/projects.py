from copy import deepcopy
from datetime import datetime
from typing import List

from sqlalchemy import select, delete
from zope.sqlalchemy import mark_changed

from wt.common import Money, Currency
from wt.fields.files import FilesModel, File
from wt.projects import ProjectsModel, Project, ProjectStatus, ProjectDoesNotExist
from wt.provider.db import DbModel
from wt.provider.db.tables import PROJECTS_TABLE
from wt.provider.db._utils import insert_or_update


class DbProjectsModel(ProjectsModel, DbModel):
    def __init__(self, session_factory, files_model: FilesModel):
        super().__init__(session_factory)
        self._files_model = files_model

    def put_project(self, project: Project):
        update_data = {
            "name": project.name,
            "status": project.status.value,
            "date_opened": project.date_opened,
            "date_closed": project.date_closed,
            "deadline": project.deadline,
            "hour_rate_amount": project.hour_rate.amount,
            "hour_rate_currency": project.hour_rate.currency.value,
            "description": project.description,
            "limitations_and_restrictions": project.limitations_and_restrictions,
            "goals_and_metrics": project.goals_and_metrics,
            "primary_color": project.primary_color,
            "secondary_color": project.secondary_color,
        }
        insert_data = deepcopy(update_data)
        insert_data["project_id"] = project.project_id
        insert_data["created_on"] = datetime.now()
        self._session.execute(
            insert_or_update(
                PROJECTS_TABLE,
                insert_data,
                update_data,
                [PROJECTS_TABLE.c.project_id]
            )
        )
        mark_changed(self._session)

        self._files_model.set_object_files(project.project_id, project.files)

    def get_project(self, project_id: str):
        query = select([PROJECTS_TABLE]).where(PROJECTS_TABLE.c.project_id == project_id)
        result = self._session.execute(query).fetchone()
        if not result:
            raise ProjectDoesNotExist(project_id)
        return self._row_to_project(
            result,
            self._files_model.get_object_files(project_id)
        )

    def get_projects(self, offset: int, limit: int):
        query = select([PROJECTS_TABLE]).offset(offset)
        query = query.limit(limit)
        query = query.order_by(PROJECTS_TABLE.c.project_id)

        result = self._session.execute(query).fetchall()
        return [
            self._row_to_project(
                row,
                self._files_model.get_object_files(row["project_id"])
            )
            for row
            in result
        ]

    def delete_project(self, project_id: str):
        query = delete(PROJECTS_TABLE).where(PROJECTS_TABLE.c.project_id == project_id)
        result = self._session.execute(query)
        if not result.rowcount:
            raise ProjectDoesNotExist(project_id)
        mark_changed(self._session)
        self._files_model.set_object_files(project_id, [])

    @staticmethod
    def _row_to_project(row: dict, files: List[File]) -> Project:
        return Project(
            project_id=row["project_id"],
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
            files=files,
        )
