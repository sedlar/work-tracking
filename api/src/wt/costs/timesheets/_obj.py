from datetime import datetime
from decimal import Decimal

from wt.ids import SimpleId


class Timesheet:
    def __init__(
            self,
            description: str,
            date_opened: datetime,
            duration: Decimal,
    ):
        self.description = description
        self.date_opened = date_opened
        self.duration = duration

    def __eq__(self, other):
        if isinstance(other, Timesheet):
            return self.__dict__ == other.__dict__
        return NotImplemented


class BoundTimesheet(Timesheet):
    def __init__(self, simple_id: SimpleId, timesheet: Timesheet):
        self.simple_id = simple_id
        super().__init__(
            description=timesheet.description,
            date_opened=timesheet.date_opened,
            duration=timesheet.duration,
        )
