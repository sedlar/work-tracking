from decimal import Decimal
from typing import List, Optional

from wt.common import Money, Currency
from wt.ids import EntityId
from wt.statistics._model import StatisticsModel
from wt.statistics._obj import Statistics, EntityStatistics


class StatisticsCalculator:
    def compute_statistics(self, entity_statistics: List[EntityStatistics]) -> Statistics:
        return Statistics(
            progress=self._compute_progress(entity_statistics),
            overall_progress=self._compute_overall_progress(entity_statistics),
            estimated_duration=self._compute_estimated_duration(entity_statistics),
            estimated_cost=self._compute_estimated_cost(entity_statistics),
            burned_duration=self._compute_burned_duration(entity_statistics),
            burned_cost=self._compute_burned_cost(entity_statistics),
            burned_expenditures_cost=self._compute_expenditures_cost(entity_statistics),
        )

    @staticmethod
    def _compute_progress(entity_statistics: List[EntityStatistics]) -> Optional[Decimal]:
        if any(statistic for statistic in entity_statistics if statistic.estimated_duration):
            return sum(
                min(
                    statistic.estimated_duration,
                    statistic.burned_duration
                ) / statistic.estimated_duration
                for statistic
                in entity_statistics
                if statistic.estimated_duration
            )
        return None

    def _compute_overall_progress(
            self,
            entity_statistics: List[EntityStatistics]
    ) -> Optional[Decimal]:
        burned_duration = self._compute_burned_duration(entity_statistics)
        estimated_duration = self._compute_estimated_duration(entity_statistics)
        if estimated_duration:
            return burned_duration / estimated_duration
        return None

    @staticmethod
    def _compute_estimated_duration(entity_statistics: List[EntityStatistics]) -> Decimal:
        return sum(
            statistic.estimated_duration
            for statistic
            in entity_statistics
            if statistic.estimated_duration
        )

    @staticmethod
    def _compute_estimated_cost(entity_statistics: List[EntityStatistics]) -> Money:
        return Money(
            amount=sum(
                statistic.estimated_duration * statistic.hour_rate.amount
                for statistic
                in entity_statistics
                if statistic.estimated_duration
            ),
            currency=Currency.czk
        )

    @staticmethod
    def _compute_burned_duration(entity_statistics: List[EntityStatistics]) -> Decimal:
        return sum(statistic.burned_duration for statistic in entity_statistics)

    @staticmethod
    def _compute_burned_cost(entity_statistics: List[EntityStatistics]) -> Money:
        return Money(
            amount=sum(
                statistic.burned_duration * statistic.hour_rate.amount
                for statistic
                in entity_statistics
            ),
            currency=Currency.czk,
        )

    @staticmethod
    def _compute_expenditures_cost(entity_statistics: List[EntityStatistics]) -> Money:
        return Money(
            amount=sum(
                statistic.expenditure_costs.amount
                for statistic
                in entity_statistics),
            currency=Currency.czk,
        )


class StatisticsApi:
    def __init__(
            self,
            statistics_model: StatisticsModel,
            statistics_calculator: StatisticsCalculator
    ):
        self._statistics_model = statistics_model
        self._statistics_calculator = statistics_calculator

    def get_project_statistics(self, project_id: EntityId) -> Statistics:
        entity_ids = self._statistics_model.get_project_ids(project_id)
        return self._compute_statistics(entity_ids)

    def get_deliverable_statistics(self, deliverable_id: EntityId) -> Statistics:
        entity_ids = self._statistics_model.get_related_entities_ids(deliverable_id)
        return self._compute_statistics(entity_ids)

    def get_entity_statistics(self, entity_id: EntityId) -> Statistics:
        entity_ids = [entity_id]
        return self._compute_statistics(entity_ids)

    def _compute_statistics(self, entity_ids: List[EntityId]) -> Statistics:
        entity_statistics = self._statistics_model.get_entity_statistics(entity_ids)
        return self._statistics_calculator.compute_statistics(entity_statistics)
