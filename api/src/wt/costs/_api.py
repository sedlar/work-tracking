from wt.common.errors import ObjectDoesNotExist, InvalidParentType
from wt.ids import EntityId, ObjectsTrackerModel
from wt.ids import EntityType


class BaseCostApi:
    _allowed_entity_types = {EntityType.issue, EntityType.meeting, EntityType.design}

    def __init__(self, objects_tracker_model: ObjectsTrackerModel):
        self._objects_tracker_model = objects_tracker_model

    def _check_type(self, entity_id: EntityId):
        parent_type = self._objects_tracker_model.get_object_type(entity_id)
        if not parent_type:
            raise ObjectDoesNotExist("Parent", entity_id)

        if parent_type not in self._allowed_entity_types:
            raise InvalidParentType(parent_type)
