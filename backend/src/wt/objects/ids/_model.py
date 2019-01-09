from typing import List, Dict

from wt.objects.ids._obj import ObjectId, ObjectType


class IdsCounterModel:
    def get_new_id(self, project_id: str) -> ObjectId:
        raise NotImplementedError()


class ObjectsTrackerModel:
    def track_object(self, object_id: ObjectId, object_type: ObjectType):
        raise NotImplementedError()

    def untrack_object(self, object_id: ObjectId):
        raise NotImplementedError()

    def get_object_type(self, object_id: ObjectId) -> ObjectType:
        raise NotImplementedError()

    def get_objects_types(self, object_ids: List[ObjectId]) -> Dict[ObjectId, ObjectType]:
        raise NotImplementedError()
