from wt.ids import EntityId
from wt.statistics._obj import Statistics
from wt.common import Money, Currency
from decimal import Decimal


ZERO = Decimal(0)
MONEY = Money(
    amount=ZERO,
    currency=Currency.czk,
)


class StatisticsApi:
    def get_project_statistics(self, project_id: EntityId) -> Statistics:
        return Statistics(
            progress=ZERO,
            estimated_duration=ZERO,
            estimated_cost=MONEY,
            burned_duration=ZERO,
            burned_cost=MONEY,
            burned_expenditures_cost=MONEY,
        )

    def get_deliverable_statistics(self, deliverable_id: EntityId) -> Statistics:
        return Statistics(
            progress=ZERO,
            estimated_duration=ZERO,
            estimated_cost=MONEY,
            burned_duration=ZERO,
            burned_cost=MONEY,
            burned_expenditures_cost=MONEY,
        )

    def get_entity_statistics(self, entity_id: EntityId) -> Statistics:
        return Statistics(
            progress=ZERO,
            estimated_duration=ZERO,
            estimated_cost=MONEY,
            burned_duration=ZERO,
            burned_cost=MONEY,
            burned_expenditures_cost=MONEY,
        )
