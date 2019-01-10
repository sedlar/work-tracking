from typing import List

from wt.common.serializers import remove_nones, serialize_datetime, deserialize_datetime
from wt.objects.deliverables._obj import Deliverable, BoundDeliverable, DeliverableStatus
from wt.objects.ids import ObjectId


class DeliverableSerializer:
    @staticmethod
    def serialize_deliverable(deliverable: BoundDeliverable) -> dict:
        return remove_nones(
            {
                "id": deliverable.object_id.object_id,
                "name": deliverable.name,
                "status": deliverable.status.value,
                "date_opened": serialize_datetime(deliverable.date_opened),
                "date_closed": serialize_datetime(deliverable.date_closed),
                "deadline": serialize_datetime(deliverable.deadline),
                "description": deliverable.description,
            }
        )

    def serialize_deliverables(self, deliverables: List[BoundDeliverable]) -> List[dict]:
        return [
            self.serialize_deliverable(deliverable)
            for deliverable
            in deliverables
        ]


class DeliverableDeserializer:
    @staticmethod
    def deserialize_deliverable(deliverable: dict) -> Deliverable:
        return Deliverable(
            name=deliverable["name"],
            status=DeliverableStatus(deliverable["status"]),
            date_opened=deserialize_datetime(deliverable["date_opened"]),
            date_closed=deserialize_datetime(deliverable.get("date_closed")),
            deadline=deserialize_datetime(deliverable.get("deadline")),
            description=deliverable["description"],
        )

    def deserialize_bound_deliverable(
            self,
            deliverable_id: str,
            deliverable: dict
    ) -> BoundDeliverable:
        return BoundDeliverable(
            object_id=ObjectId(deliverable_id),
            deliverable=self.deserialize_deliverable(deliverable)
        )
