from typing import List, Dict, Optional

from wt.entities.ids._obj import EntityId, ObjectType


class IdsCounterModel:
    def get_new_id(self, project_id: EntityId) -> EntityId:
        raise NotImplementedError()

    def drop_project(self, project_id: EntityId):
        raise NotImplementedError()


class ObjectsTrackerModel:
    def track_object(self, object_id: EntityId, object_type: ObjectType):
        raise NotImplementedError()

    def untrack_object(self, object_id: EntityId):
        raise NotImplementedError()

    def get_object_type(self, object_id: EntityId) -> Optional[ObjectType]:
        raise NotImplementedError()

    def get_objects_types(self, object_ids: List[EntityId]) -> Dict[EntityId, ObjectType]:
        raise NotImplementedError()

    def get_objects_types_by_project(self, project_id: str) -> Dict[EntityId, ObjectType]:
        raise NotImplementedError()
