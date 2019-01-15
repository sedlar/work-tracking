from typing import List

from wt.costs.timesheets._obj import Timesheet, BoundTimesheet
from wt.ids import SimpleId, EntityId


class TimesheetsModel:
    def create_timesheet(self, entity_id: EntityId, timesheet: Timesheet) -> BoundTimesheet:
        raise NotImplementedError()

    def delete_timesheet(self, timesheet_id: SimpleId):
        raise NotImplementedError()

    def delete_entity_timesheets(self, entity_id: EntityId):
        raise NotImplementedError()

    def get_timesheets(self, entity_id: EntityId, offset: int, limit: int) -> List[BoundTimesheet]:
        raise NotImplementedError()
