from typing import List, Optional

from wt.entities._entity_manager import EntityManager
from wt.entities.deliverables._errors import DeliverableDoesNotExist
from wt.entities.deliverables._model import DeliverablesModel
from wt.entities.deliverables._obj import Deliverable, BoundDeliverable
from wt.ids import EntityId, EntityType
from wt.links import EntityLinksModel


class DeliverablesApi:
    def __init__(
            self,
            deliverables_model: DeliverablesModel,
            entity_manager: EntityManager,
            entity_links_model: EntityLinksModel,
    ):
        self._deliverable_model = deliverables_model
        self._entity_manager = entity_manager
        self._entity_links_model = entity_links_model

    def create_deliverable(
            self,
            project_id: EntityId,
            deliverable: Deliverable
    ) -> BoundDeliverable:
        deliverable_id = self._entity_manager.create_entity(project_id, EntityType.deliverable)
        bound_deliverable = BoundDeliverable(deliverable_id, deliverable)
        self._deliverable_model.put_deliverable(bound_deliverable)
        return bound_deliverable

    def edit_deliverable(self, deliverable: BoundDeliverable):
        if not self._entity_manager.check_entity_type(
                deliverable.object_id,
                EntityType.deliverable
        ):
            raise DeliverableDoesNotExist(deliverable.object_id)
        self._deliverable_model.put_deliverable(deliverable)

    def get_deliverable(self, deliverable_id: EntityId) -> BoundDeliverable:
        return self._deliverable_model.get_deliverable(deliverable_id)

    def get_deliverables(
            self,
            project_id: Optional[EntityId],
            related_entity_id: Optional[EntityId],
            offset: int,
            limit: int,
    ) -> List[BoundDeliverable]:
        return self._deliverable_model.get_deliverables(
            project_id,
            related_entity_id,
            offset,
            limit
        )

    def delete_deliverable(self, deliverable_id: EntityId):
        self._entity_links_model.delete_links(deliverable_id)
        self._deliverable_model.delete_deliverable(deliverable_id)
        self._entity_manager.delete_entity(deliverable_id)
