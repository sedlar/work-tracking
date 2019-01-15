from typing import List

from wt.costs.expenditures._obj import Expenditure, BoundExpenditure
from wt.ids import SimpleId, EntityId


class ExpendituresModel:
    def create_expenditure(self, entity_id: EntityId, expenditure: Expenditure) -> BoundExpenditure:
        raise NotImplementedError()

    def delete_expenditure(self, expenditure_id: SimpleId):
        raise NotImplementedError()

    def delete_entity_expenditures(self, entity_id: EntityId):
        raise NotImplementedError()

    def get_expenditures(
            self,
            entity_id: EntityId,
            offset: int,
            limit: int
    ) -> List[BoundExpenditure]:
        raise NotImplementedError()
