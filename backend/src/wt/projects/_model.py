from typing import List

from wt.projects._obj import Project


class ProjectsModel:
    def put_project(self, project: Project):
        raise NotImplementedError()

    def get_project(self, project_id: str) -> Project:
        raise NotImplementedError()

    def get_projects(self, offset: int, limit: int) -> List[Project]:
        raise NotImplementedError()

    def delete_project(self, project_id: str):
        raise NotImplementedError()
