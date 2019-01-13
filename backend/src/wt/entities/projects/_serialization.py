from typing import List

from wt.common.serializers import remove_nones, serialize_datetime, deserialize_datetime, \
    serialize_money, deserialize_money
from wt.entities.projects._obj import Project, ProjectStatus
from wt.fields.files import FileDeserializer, FileSerializer
from wt.ids import EntityId


class ProjectSerializer:
    def __init__(self, files_serializer: FileSerializer):
        self._files_serializer = files_serializer

    def serialize_project(self, project: Project) -> dict:
        return remove_nones(
            {
                "id": project.project_id.project_id,
                "name": project.name,
                "status": project.status.value,
                "date_opened": serialize_datetime(project.date_opened),
                "date_closed": serialize_datetime(project.date_closed),
                "deadline": serialize_datetime(project.deadline),
                "hour_rate": serialize_money(project.hour_rate),
                "description": project.description,
                "goals_and_metrics": project.goals_and_metrics,
                "limitations_and_restrictions": project.limitations_and_restrictions,
                "files": self._files_serializer.serialize_files(project.files),
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


class ProjectDeserializer:
    def __init__(self, files_deserializer: FileDeserializer):
        self._files_deserializer = files_deserializer

    def deserialize_project(self, project_id: str, project: dict) -> Project:
        return Project(
            project_id=EntityId(project_id),
            name=project["name"],
            status=ProjectStatus(project["status"]),
            date_opened=deserialize_datetime(project["date_opened"]),
            date_closed=deserialize_datetime(project.get("date_closed")),
            deadline=deserialize_datetime(project.get("deadline")),
            hour_rate=deserialize_money(project["hour_rate"]),
            description=project["description"],
            goals_and_metrics=project["goals_and_metrics"],
            limitations_and_restrictions=project["limitations_and_restrictions"],
            files=self._files_deserializer.deserialize_files(project["files"]),
            primary_color=project["primary_color"],
            secondary_color=project["secondary_color"],
        )
