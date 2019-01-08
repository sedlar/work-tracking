from typing import List

from wt.projects._model import ProjectsModel
from wt.projects._obj import Project


class ProjectsApi:
    def __init__(self, project_model: ProjectsModel):
        self._project_model = project_model

    def put_project(self, project: Project):
        self._project_model.put_project(project)

    def get_project(self, project_id: str) -> Project:
        return self._project_model.get_project(project_id)

    def get_projects(self, offset: int, limit: int) -> List[Project]:
        return self._project_model.get_projects(offset, limit)

    def delete_project(self, project_id: str):
        self._project_model.delete_project(project_id)
