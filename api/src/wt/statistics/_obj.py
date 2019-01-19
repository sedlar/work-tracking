from wt.common import Money
from decimal import Decimal


class Statistics:
    def __init__(
            self,
            progress: Decimal,
            estimated_duration: Decimal,
            estimated_cost: Money,
            burned_duration: Decimal,
            burned_cost: Money,
            burned_expenditures_cost: Money,
    ):
        self.progress = progress
        self.estimated_duration = estimated_duration
        self.estimated_cost = estimated_cost
        self.burned_duration = burned_duration
        self.burned_cost = burned_cost
        self.burned_expenditures_cost = burned_expenditures_cost
