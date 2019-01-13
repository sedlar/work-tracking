from typing import List

from wt.entities.deliverables._obj import BoundDeliverable
from wt.ids import EntityId


class DeliverablesModel:
    def put_deliverable(self, deliverable: BoundDeliverable):
        raise NotImplementedError()

    def get_deliverable(self, deliverable_id: EntityId) -> BoundDeliverable:
        raise NotImplementedError()

    def get_deliverables(
            self,
            project_id: EntityId,
            offset: int,
            limit: int
    ) -> List[BoundDeliverable]:
        raise NotImplementedError()

    def delete_deliverable(self, deliverable_id: EntityId):
        raise NotImplementedError()
