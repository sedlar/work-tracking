from collections import namedtuple
from typing import List
from decimal import Decimal

from sqlalchemy import select, func

from wt.common import Money, Currency
from wt.costs.expenditures import ExpenditureStatus
from wt.ids import EntityId, EntityType
from wt.provider.db import DbModel
from wt.provider.db.tables import (
    OBJECTS_TRACKER_TABLE,
    ENTITY_LINKS_TABLE,
    ISSUES_TABLE,
    PROJECTS_TABLE,
    TIMESHEETS_TABLE,
    EXPENDITURES_TABLE,
)
from wt.statistics import StatisticsModel, EntityStatistics

EntityStatisticsData = namedtuple("EntityStatisticsData", ["hour_rate", "estimated_duration"])


class DbStatisticsModel(StatisticsModel, DbModel):
    def get_project_ids(self, project_id: EntityId):
        query = select(
            [OBJECTS_TRACKER_TABLE.c.id]
        ).where(
            OBJECTS_TRACKER_TABLE.c.project_id == project_id.full_id
        ).where(
            OBJECTS_TRACKER_TABLE.c.type != EntityType.project.value
        )
        result = self._session.execute(query)
        return [
            EntityId(row["id"])
            for row
            in result
        ]

    def get_related_entities_ids(self, entity_id: EntityId):
        query = select(
            [ENTITY_LINKS_TABLE.c.object_id]
        ).where(
            ENTITY_LINKS_TABLE.c.other_object_id == entity_id.full_id
        )
        result = self._session.execute(query)
        return [
            EntityId(row["object_id"])
            for row
            in result
        ]

    def get_entity_statistics(self, entity_ids: List[EntityId]):
        if not entity_ids:
            return []
        assert len({entity_id.project_id for entity_id in entity_ids}) == 1

        full_ids = [entity_id.full_id for entity_id in entity_ids]
        # All entities are from same project
        default_hour_rate = self._get_project_hour_rate(entity_ids[0].project_id)
        entity_data = self._get_entity_data(full_ids)
        burned_time = self._get_burned_time(full_ids)
        expenditure_costs = self._get_expenditure_costs(full_ids)

        entity_statistics = []
        for entity_id in entity_ids:
            hour_rate = default_hour_rate
            if entity_data[entity_id].hour_rate:
                hour_rate = entity_data[entity_id].hour_rate
            entity_statistics.append(
                EntityStatistics(
                    estimated_duration=entity_data[entity_id].estimated_duration,
                    hour_rate=hour_rate,
                    burned_duration=burned_time.get(entity_id, Decimal(0)),
                    expenditure_costs=expenditure_costs.get(
                        entity_id,
                        Money(
                            amount=Decimal(0),
                            currency=Currency.czk,
                        )
                    ),
                )
            )
        return entity_statistics

    def _get_entity_data(self, entity_ids: List[str]):
        query = select(
            [
                ISSUES_TABLE.c.hour_rate_amount,
                ISSUES_TABLE.c.hour_rate_currency,
                ISSUES_TABLE.c.estimated_duration,
                ISSUES_TABLE.c.object_id,
            ]
        ).where(
            ISSUES_TABLE.c.object_id.in_(entity_ids)
        )
        result = self._session.execute(query)
        entity_data = {}
        for row in result:
            amount = row["hour_rate_amount"]
            currency = row["hour_rate_currency"]
            hour_rate = None
            if amount is not None and currency:
                hour_rate = Money(
                    amount=amount,
                    currency=currency,
                )
            entity_data[EntityId(row["object_id"])] = EntityStatisticsData(
                hour_rate=hour_rate,
                estimated_duration=row["estimated_duration"]
            )
        return entity_data

    def _get_burned_time(self, entity_ids: List[str]):
        query = select(
            [
                TIMESHEETS_TABLE.c.parent_id,
                func.sum(TIMESHEETS_TABLE.c.duration).label("burned_duration"),
            ]
        ).group_by(
            TIMESHEETS_TABLE.c.parent_id
        ).where(
            TIMESHEETS_TABLE.c.parent_id.in_(entity_ids)
        )
        result = self._session.execute(query)
        return {
            EntityId(row["parent_id"]): row["burned_duration"]
            for row
            in result
        }

    def _get_expenditure_costs(self, entity_ids: List[str]):
        query = select(
            [
                EXPENDITURES_TABLE.c.parent_id,
                func.sum(EXPENDITURES_TABLE.c.cost_amount).label("expenditure_costs"),
            ]
        ).group_by(
            EXPENDITURES_TABLE.c.parent_id
        ).where(
            EXPENDITURES_TABLE.c.parent_id.in_(entity_ids)
        ).where(
            EXPENDITURES_TABLE.c.status == ExpenditureStatus.approved.value
        )
        result = self._session.execute(query)
        return {
            EntityId(row["parent_id"]): Money(
                amount=row["expenditure_costs"],
                currency=Currency.czk,
            )
            for row
            in result
        }

    def _get_project_hour_rate(self, project_id: str):
        query = select(
            [
                PROJECTS_TABLE.c.hour_rate_amount,
                PROJECTS_TABLE.c.hour_rate_currency,
            ]
        ).where(
            PROJECTS_TABLE.c.project_id == project_id
        )
        row = self._session.execute(query).fetchone()
        return Money(
            amount=row["hour_rate_amount"],
            currency=Currency(row["hour_rate_currency"]),
        )
