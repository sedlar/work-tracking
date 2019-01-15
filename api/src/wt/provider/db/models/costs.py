from datetime import datetime
from typing import List

from sqlalchemy import insert, delete, select
from zope.sqlalchemy import mark_changed

from wt.common import Money, Currency
from wt.costs.expenditures import (
    ExpenditureType,
    ExpenditureStatus,
    Expenditure,
    ExpendituresModel,
    BoundExpenditure,
)
from wt.costs.timesheets import Timesheet, BoundTimesheet, TimesheetsModel
from wt.fields.files import FilesModel
from wt.ids import SimpleId, EntityId, SimpleEntityType
from wt.provider.db import DbModel
from wt.provider.db.tables import TIMESHEETS_TABLE, EXPENDITURES_TABLE


class BaseCostsModel(DbModel):
    _table = None

    def _create_cost(self, entity_id, cost):
        data = self._cost_to_dict(cost)
        data["parent_id"] = entity_id.full_id
        data["created_on"] = datetime.now()
        query = insert(self._table).values(data)
        result = self._session.execute(query)
        mark_changed(self._session)
        return result.inserted_primary_key[0]

    def _delete_cost(self, cost_id: SimpleId):
        query = delete(self._table).where(self._table.c.id == cost_id.simple_id)
        self._session.execute(query)
        mark_changed(self._session)

    def _delete_entity_costs(self, entity_id: EntityId):
        query = delete(self._table).where(self._table.c.parent_id == entity_id.full_id)
        self._session.execute(query)
        mark_changed(self._session)

    def _get_costs(self, entity_id: EntityId, offset: int, limit: int):
        query = (
            select([self._table])
            .where(self._table.c.parent_id == entity_id.full_id)
            .order_by(self._table.c.created_on)
            .offset(offset)
            .limit(limit)
        )
        result = self._session.execute(query)
        return [
            self._row_to_cost(row)
            for row
            in result
        ]

    @staticmethod
    def _cost_to_dict(cost):
        raise NotImplementedError()

    @staticmethod
    def _row_to_cost(row):
        raise NotImplementedError()


class DbTimesheetsModel(BaseCostsModel, TimesheetsModel):
    _table = TIMESHEETS_TABLE

    def create_timesheet(self, entity_id: EntityId, timesheet: Timesheet) -> BoundTimesheet:
        timesheet_id = self._create_cost(entity_id, timesheet)
        return BoundTimesheet(SimpleId(SimpleEntityType.timesheet, timesheet_id), timesheet)

    def delete_timesheet(self, timesheet_id: SimpleId):
        self._delete_cost(timesheet_id)

    def delete_entity_timesheets(self, entity_id: EntityId):
        self._delete_entity_costs(entity_id)

    def get_timesheets(self, entity_id: EntityId, offset: int, limit: int) -> List[BoundTimesheet]:
        return self._get_costs(entity_id, offset, limit)

    @staticmethod
    def _cost_to_dict(cost):
        return {
            "description": cost.description,
            "duration": cost.duration,
            "date_opened": cost.date_opened,
        }

    @staticmethod
    def _row_to_cost(row):
        return BoundTimesheet(
            SimpleId(SimpleEntityType.timesheet, row["id"]),
            Timesheet(
                description=row["description"],
                duration=row["duration"],
                date_opened=row["date_opened"],
            )
        )


class DbExpendituresModel(BaseCostsModel, ExpendituresModel):
    _table = EXPENDITURES_TABLE

    def __init__(self, session_factory, files_model: FilesModel):
        super().__init__(session_factory)
        self._files_model = files_model

    def create_expenditure(self, entity_id: EntityId, expenditure: Expenditure) -> BoundExpenditure:
        simple_id = self._create_cost(entity_id, expenditure)
        expenditure_id = SimpleId(SimpleEntityType.expenditure, simple_id)
        self._files_model.set_entity_files(expenditure_id, expenditure.files)
        return BoundExpenditure(expenditure_id, expenditure)

    def delete_expenditure(self, expenditure_id: SimpleId):
        self._files_model.set_entity_files(expenditure_id, [])
        self._delete_cost(expenditure_id)

    def delete_entity_expenditures(self, entity_id: EntityId):
        self._delete_entity_costs(entity_id)

    def get_expenditures(
            self,
            entity_id: EntityId,
            offset: int,
            limit: int
    ) -> List[BoundExpenditure]:
        expenditures = self._get_costs(entity_id, offset, limit)
        for expenditure in expenditures:
            expenditure.files = self._files_model.get_entity_files(expenditure.simple_id)
        return expenditures

    @staticmethod
    def _row_to_cost(row):
        return BoundExpenditure(
            simple_id=SimpleId(SimpleEntityType.expenditure, row["id"]),
            expenditure=Expenditure(
                name=row["name"],
                description=row["description"],
                status=ExpenditureStatus(row["status"]),
                type_=ExpenditureType(row["type"]),
                date_opened=row["date_opened"],
                date_closed=row["date_closed"],
                deadline=row["deadline"],
                files=[],
                cost=Money(
                    amount=row["cost_amount"],
                    currency=Currency(row["cost_currency"]),
                )
            )
        )

    @staticmethod
    def _cost_to_dict(cost: Expenditure):
        return {
            "name": cost.name,
            "description": cost.description,
            "status": cost.status.value,
            "type": cost.type.value,
            "date_opened": cost.date_opened,
            "date_closed": cost.date_closed,
            "deadline": cost.deadline,
            "cost_amount": cost.cost.amount,
            "cost_currency": cost.cost.currency.value,
        }
