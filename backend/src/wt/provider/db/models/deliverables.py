from copy import deepcopy
from typing import List
from datetime import datetime

from sqlalchemy import select, delete
from zope.sqlalchemy import mark_changed

from wt.entities.deliverables import DeliverableDoesNotExist
from wt.entities.deliverables import (
    DeliverablesModel,
    BoundDeliverable,
    DeliverableStatus,
    Deliverable,
)
from wt.entities.ids import EntityId
from wt.provider.db import DbModel
from wt.provider.db.tables import DELIVERABLES_TABLE
from wt.provider.db._utils import insert_or_update


class DbDeliverablesModel(DeliverablesModel, DbModel):
    def put_deliverable(self, deliverable: BoundDeliverable):
        update_data = {
            "project_id": deliverable.object_id.project_id,
            "name": deliverable.name,
            "status": deliverable.status.value,
            "description": deliverable.description,
            "date_opened": deliverable.date_opened,
            "date_closed": deliverable.date_closed,
            "deadline": deliverable.deadline,
        }
        insert_data = deepcopy(update_data)
        insert_data["object_id"] = deliverable.object_id.full_id
        insert_data["created_on"] = datetime.now()
        self._session.execute(
            insert_or_update(
                DELIVERABLES_TABLE,
                insert_data,
                update_data,
                [DELIVERABLES_TABLE.c.object_id]
            )
        )
        mark_changed(self._session)

    def delete_deliverable(self, object_id: EntityId):
        query = delete(DELIVERABLES_TABLE)
        query = query.where(DELIVERABLES_TABLE.c.object_id == object_id.full_id)
        result = self._session.execute(query)
        if not result.rowcount:
            raise DeliverableDoesNotExist(object_id)
        mark_changed(self._session)

    def get_deliverable(self, object_id: EntityId) -> BoundDeliverable:
        query = select([DELIVERABLES_TABLE])
        query = query.where(DELIVERABLES_TABLE.c.object_id == object_id.full_id)
        result = self._session.execute(query).fetchone()

        if not result:
            raise DeliverableDoesNotExist(object_id)

        return self._row_to_deliverable(result)

    def get_deliverables(
            self,
            project_id: EntityId,
            offset: int,
            limit: int
    ) -> List[BoundDeliverable]:
        query = select([DELIVERABLES_TABLE]).offset(offset)
        query = query.where(DELIVERABLES_TABLE.c.project_id == project_id.project_id)
        query = query.limit(limit)
        query = query.order_by(DELIVERABLES_TABLE.c.created_on)

        result = self._session.execute(query).fetchall()
        return [
            self._row_to_deliverable(row)
            for row
            in result
        ]

    @staticmethod
    def _row_to_deliverable(row) -> BoundDeliverable:
        return BoundDeliverable(
            object_id=EntityId(row["object_id"]),
            deliverable=Deliverable(
                name=row["name"],
                status=DeliverableStatus(row["status"]),
                date_opened=row["date_opened"],
                date_closed=row["date_closed"],
                deadline=row["deadline"],
                description=row["description"],
            )
        )
