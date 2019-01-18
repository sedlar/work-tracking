from decimal import Decimal
from typing import List

from wt.costs.timesheets._obj import BoundTimesheet, Timesheet


class TimesheetsSerializer:
    @staticmethod
    def serialize_timesheet(timesheet: BoundTimesheet):
        return {
            "id": timesheet.simple_id.simple_id,
            "duration": timesheet.duration,
            "description": timesheet.description,
            "date_opened": timesheet.date_opened,
        }

    def serialize_timesheets(self, timesheets: List[BoundTimesheet]):
        return [
            self.serialize_timesheet(timesheet)
            for timesheet
            in timesheets
        ]


class TimesheetsDeserializer:
    @staticmethod
    def deserialize_timesheet(timesheet) -> Timesheet:
        return Timesheet(
            description=timesheet["description"],
            duration=Decimal(timesheet["duration"]),
            date_opened=timesheet["date_opened"],
        )
