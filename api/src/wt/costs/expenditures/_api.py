from typing import List

from wt.costs._api import BaseCostApi
from wt.costs.expenditures._model import ExpendituresModel
from wt.costs.expenditures._obj import Expenditure, BoundExpenditure
from wt.ids import EntityId, ObjectsTrackerModel, SimpleId


class ExpendituresApi(BaseCostApi):
    def __init__(
            self,
            objects_tracker_model: ObjectsTrackerModel,
            expenditures_model: ExpendituresModel,
    ):
        super().__init__(objects_tracker_model)
        self._expenditures_model = expenditures_model

    def create_expenditure(self, entity_id: EntityId, expenditure: Expenditure):
        self._check_type(entity_id)
        return self._expenditures_model.create_expenditure(entity_id, expenditure)

    def delete_expenditure(self, expenditure_id: SimpleId):
        self._expenditures_model.delete_expenditure(expenditure_id)

    def get_expenditures(
            self,
            entity_id: EntityId,
            offset: int,
            limit: int
    ) -> List[BoundExpenditure]:
        return self._expenditures_model.get_expenditures(entity_id, offset, limit)
