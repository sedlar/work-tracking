from typing import List

from wt.entities.projects._model import ProjectsModel
from wt.entities.projects._obj import Project
from wt.ids import IdsCounterModel, ObjectsTrackerModel, EntityId, EntityType
from wt.entities.projects._errors import ProjectHasChildElements


class ProjectsApi:
    def __init__(
            self,
            project_model: ProjectsModel,
            ids_counter_model: IdsCounterModel,
            objects_tracker_model: ObjectsTrackerModel,
    ):
        self._project_model = project_model
        self._ids_counter_model = ids_counter_model
        self._objects_tracker_model = objects_tracker_model

    def put_project(self, project: Project):
        object_type = self._objects_tracker_model.get_object_type(project.project_id)
        if not object_type:
            self._objects_tracker_model.track_object(project.project_id, EntityType.project)
        self._project_model.put_project(project)

    def get_project(self, project_id: EntityId) -> Project:
        return self._project_model.get_project(project_id)

    def get_projects(self, offset: int, limit: int) -> List[Project]:
        return self._project_model.get_projects(offset, limit)

    def delete_project(self, project_id: EntityId):
        object_types_map = self._objects_tracker_model.get_objects_types_by_project(project_id)
        if object_types_map:
            raise ProjectHasChildElements(set(object_types_map.values()))

        self._project_model.delete_project(project_id)
        self._ids_counter_model.drop_project(project_id)
        self._objects_tracker_model.untrack_object(project_id)
