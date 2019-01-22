from decimal import Decimal

from wt.common import Money


class EntityStatistics:
    def __init__(
            self,
            estimated_duration: Decimal,
            hour_rate: Money,
            burned_duration: Decimal,
            expenditure_costs: Money,
    ):
        self.estimated_duration = estimated_duration
        self.hour_rate = hour_rate
        self.burned_duration = burned_duration
        self.expenditure_costs = expenditure_costs


class Statistics:
    def __init__(
            self,
            progress: Decimal,
            overall_progress: Decimal,
            estimated_duration: Decimal,
            estimated_cost: Money,
            burned_duration: Decimal,
            burned_cost: Money,
            burned_expenditures_cost: Money,
    ):
        # pylint: disable=too-many-arguments
        self.progress = progress
        self.overall_progress = overall_progress
        self.estimated_duration = estimated_duration
        self.estimated_cost = estimated_cost
        self.burned_duration = burned_duration
        self.burned_cost = burned_cost
        self.burned_expenditures_cost = burned_expenditures_cost
