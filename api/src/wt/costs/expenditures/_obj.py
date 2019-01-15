from datetime import datetime
from enum import Enum
from typing import Optional, List

from wt.common import Money
from wt.ids import SimpleId


class ExpenditureStatus(Enum):
    submitted = "submitted"
    approved = "approved"
    reimbudes = "reimbudes"


class ExpenditureType(Enum):
    hosting = "hosting"
    code = "code"
    artwork = "artwork"
    stock = "stock"
    photos = "photos"
    freelance = "freelance"
    room = "room"
    transport = "transport"
    other = "other"


class Expenditure:
    # pylint: disable=too-many-instance-attributes
    def __init__(
            self,
            name: str,
            status: ExpenditureStatus,
            type_: ExpenditureType,
            description: str,
            date_opened: datetime,
            date_closed: Optional[datetime],
            deadline: Optional[datetime],
            files: List[str],
            cost: Money,
    ):
        # pylint: disable=too-many-arguments
        self.name = name
        self.status = status
        self.type = type_
        self.description = description
        self.date_opened = date_opened
        self.date_closed = date_closed
        self.deadline = deadline
        self.files = files
        self.cost = cost

    def __eq__(self, other):
        if isinstance(other, Expenditure):
            return self.__dict__ == other.__dict__
        return NotImplemented


class BoundExpenditure(Expenditure):
    def __init__(self, simple_id: SimpleId, expenditure):
        self.simple_id = simple_id
        super().__init__(
            name=expenditure.name,
            status=expenditure.status,
            type_=expenditure.type,
            description=expenditure.description,
            date_opened=expenditure.date_opened,
            date_closed=expenditure.date_closed,
            deadline=expenditure.deadline,
            files=expenditure.files,
            cost=expenditure.cost,
        )
