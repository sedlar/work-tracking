from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from dateutil import parser

from wt.common import Money, Currency
from wt.common import remove_nones
from wt.files import File
from wt.projects._obj import Project, ProjectStatus


class ProjectSerializer:
    def serialize_project(self, project: Project) -> dict:
        return remove_nones(
            {
                "id": project.project_id,
                "name": project.name,
                "status": project.status.value,
                "date_opened": self.serialize_datetime(project.date_opened),
                "date_closed": self.serialize_datetime(project.date_closed),
                "deadline": self.serialize_datetime(project.deadline),
                "hour_rate": self.serialize_money(project.hour_rate),
                "description": project.description,
                "goals_and_metrics": project.goals_and_metrics,
                "limitations_and_restrictions": project.limitations_and_restrictions,
                "files": self.serialize_files(project.files),
                "primary_color": project.primary_color,
                "secondary_color": project.secondary_color,
            }
        )

    def serialize_projects(self, projects: List[Project]) -> List[dict]:
        return [
            self.serialize_project(project)
            for project
            in projects
        ]

    @staticmethod
    def serialize_datetime(timestamp: Optional[datetime]) -> Optional[str]:
        if timestamp is not None:
            return timestamp.isoformat()
        return None

    @staticmethod
    def serialize_files(files: List[File]) -> List[str]:
        return [file.uri for file in files]

    @staticmethod
    def serialize_money(money: Money) -> dict:
        return {
            "amount": money.amount,
            "currency": money.currency.value,
        }


class ProjectDeserializer:
    def deserialize_project(self, project_id: str, project: dict) -> Project:
        return Project(
            project_id=project_id,
            name=project["name"],
            status=ProjectStatus(project["status"]),
            date_opened=self.deserialize_datetime(project["date_opened"]),
            date_closed=self.deserialize_datetime(project.get("date_closed")),
            deadline=self.deserialize_datetime(project.get("deadline")),
            hour_rate=self.deserialize_money(project["hour_rate"]),
            description=project["description"],
            goals_and_metrics=project["goals_and_metrics"],
            limitations_and_restrictions=project["limitations_and_restrictions"],
            files=self.deserialize_files(project["files"]),
            primary_color=project["primary_color"],
            secondary_color=project["secondary_color"],
        )

    @staticmethod
    def deserialize_files(files: List[str]) -> List[File]:
        return [File(file) for file in files]

    @staticmethod
    def deserialize_datetime(serialized_timestamp: Optional[str]) -> Optional[datetime]:
        if serialized_timestamp:
            return parser.parse(serialized_timestamp)
        return None

    @staticmethod
    def deserialize_money(money: dict) -> Money:
        return Money(
            amount=Decimal(money["amount"]),
            currency=Currency(money["currency"]),
        )
