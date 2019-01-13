from typing import List
from wt.ids import EntityId, ObjectType

from wt.entities.deliverables._model import DeliverablesModel
from wt.entities.deliverables._obj import Deliverable, BoundDeliverable
from wt.entities.deliverables._errors import DeliverableDoesNotExist
from wt.ids import IdsCounterModel, ObjectsTrackerModel


class DeliverablesApi:
    def __init__(
            self,
            deliverables_model: DeliverablesModel,
            ids_counter_model: IdsCounterModel,
            objects_tracker_model: ObjectsTrackerModel
    ):
        self._deliverable_model = deliverables_model
        self._ids_counter_model = ids_counter_model
        self._objects_tracker_model = objects_tracker_model

    def create_deliverable(
            self,
            project_id: EntityId,
            deliverable: Deliverable
    ) -> BoundDeliverable:
        deliverable_id = self._ids_counter_model.get_new_id(project_id)
        bound_deliverable = BoundDeliverable(deliverable_id, deliverable)
        self._deliverable_model.put_deliverable(bound_deliverable)
        self._objects_tracker_model.track_object(deliverable_id, ObjectType.deliverable)
        return bound_deliverable

    def edit_deliverable(self, deliverable: BoundDeliverable):
        object_type = self._objects_tracker_model.get_object_type(deliverable.object_id)
        if object_type != ObjectType.deliverable:
            raise DeliverableDoesNotExist(deliverable.object_id)
        self._deliverable_model.put_deliverable(deliverable)

    def get_deliverable(self, deliverable_id: EntityId) -> BoundDeliverable:
        return self._deliverable_model.get_deliverable(deliverable_id)

    def get_deliverables(
            self,
            project_id: EntityId,
            offset: int,
            limit: int
    ) -> List[BoundDeliverable]:
        return self._deliverable_model.get_deliverables(project_id, offset, limit)

    def delete_deliverable(self, deliverable_id: EntityId):
        self._deliverable_model.delete_deliverable(deliverable_id)
        self._objects_tracker_model.untrack_object(deliverable_id)