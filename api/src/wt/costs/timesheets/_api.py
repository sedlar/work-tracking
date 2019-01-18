from typing import List

from wt.costs._api import BaseCostApi
from wt.costs.timesheets._model import TimesheetsModel
from wt.costs.timesheets._obj import Timesheet, BoundTimesheet
from wt.ids import EntityId, ObjectsTrackerModel, SimpleId


class TimesheetsApi(BaseCostApi):
    def __init__(
            self,
            objects_tracker_model: ObjectsTrackerModel,
            timesheets_model: TimesheetsModel,
    ):
        super().__init__(objects_tracker_model)
        self._timesheets_model = timesheets_model

    def create_timesheet(self, entity_id: EntityId, timesheet: Timesheet):
        self._check_type(entity_id)
        return self._timesheets_model.create_timesheet(entity_id, timesheet)

    def delete_timesheet(self, timesheet_id: SimpleId):
        self._timesheets_model.delete_timesheet(timesheet_id)

    def get_timesheets(
            self,
            entity_id: EntityId,
            offset: int,
            limit: int
    ) -> List[BoundTimesheet]:
        return self._timesheets_model.get_timesheets(entity_id, offset, limit)
