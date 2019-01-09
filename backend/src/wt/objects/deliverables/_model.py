from typing import List

from wt.objects.deliverables._obj import BoundDeliverable
from wt.objects.ids import ObjectId


class DeliverablesModel:
    def put_deliverable(self, deliverable: BoundDeliverable):
        raise NotImplementedError()

    def get_deliverable(self, object_id: ObjectId) -> BoundDeliverable:
        raise NotImplementedError()

    def get_deliverables(self, offset: int, limit: int) -> List[BoundDeliverable]:
        raise NotImplementedError()

    def delete_deliverable(self, object_id: ObjectId):
        raise NotImplementedError()
