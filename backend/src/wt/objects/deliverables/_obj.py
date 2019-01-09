from datetime import datetime
from enum import Enum
from wt.objects.ids import ObjectId


class DeliverableStatus(Enum):
    pending = "pending"
    open = "open"
    completed = "completed"
    archived = "archived"


class Deliverable:
    def __init__(
            self,
            name: str,
            status: DeliverableStatus,
            description: str,
            date_opened: datetime,
            date_closed: datetime,
            deadline: datetime,
    ):
        # pylint: disable=too-many-arguments
        self.name = name
        self.status = status
        self.description = description
        self.date_opened = date_opened
        self.date_closed = date_closed
        self.deadline = deadline

    def __eq__(self, other):
        if isinstance(other, Deliverable):
            return self.__dict__ == other.__dict__

        return NotImplemented


class BoundDeliverable(Deliverable):
    def __init__(self, object_id: ObjectId, deliverable):
        self.object_id = object_id
        super().__init__(
            name=deliverable.name,
            status=deliverable.status,
            description=deliverable.description,
            date_opened=deliverable.date_opened,
            date_closed=deliverable.date_closed,
            deadline=deliverable.deadline,
        )
