from typing import List

from wt.entities.projects._obj import Project
from wt.ids import EntityId


class ProjectsModel:
    def put_project(self, project: Project):
        raise NotImplementedError()

    def get_project(self, project_id: EntityId) -> Project:
        raise NotImplementedError()

    def get_projects(self, offset: int, limit: int) -> List[Project]:
        raise NotImplementedError()

    def delete_project(self, project_id: EntityId):
        raise NotImplementedError()
