from wt.entities.projects import ProjectDoesNotExist
from wt.ids import EntityType, EntityId
from wt.ids import IdsCounterModel, ObjectsTrackerModel


class EntityManager:
    def __init__(
            self,
            ids_counter_model: IdsCounterModel,
            objects_tracker_model: ObjectsTrackerModel,
    ):
        self._ids_counter_model = ids_counter_model
        self._objects_tracker_model = objects_tracker_model

    def create_entity(self, project_id: EntityId, entity_type: EntityType) -> EntityId:
        object_type = self._objects_tracker_model.get_object_type(project_id)
        if object_type != EntityType.project:
            raise ProjectDoesNotExist(project_id)
        entity_id = self._ids_counter_model.get_new_id(project_id)
        self._objects_tracker_model.track_object(entity_id, entity_type)
        return entity_id

    def check_entity_type(self, entity_id: EntityId, entity_type: EntityType) -> bool:
        object_type = self._objects_tracker_model.get_object_type(entity_id)
        return object_type == entity_type

    def delete_entity(self, entity_id: EntityId):
        self._objects_tracker_model.untrack_object(entity_id)
