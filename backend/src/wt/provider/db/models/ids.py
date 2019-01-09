from typing import List, Dict

from sqlalchemy import Table, Column, select, delete, update, insert, String, Integer
from zope.sqlalchemy import mark_changed

from wt.objects.ids import (
    IdsCounterModel,
    ObjectId,
    ObjectType,
    ObjectsTrackerModel,
    ObjectsDoesNotExist
)
from wt.provider.db import DbModel, METADATA
from wt.provider.db._utils import get_enum_length
from wt.provider.db._columns import PROJECT_ID_COLUMN_REFERENCE, ID_COLUMN_TYPE
from copy import deepcopy

IDS_COUNTER_TABLE = Table(
    "ids_counter",
    METADATA,
    Column("project_id", ID_COLUMN_TYPE, primary_key=True),
    Column("next_id", Integer(), nullable=False),
)

OBJECTS_TRACKER_TABLE = Table(
    "objects_tracker",
    METADATA,
    Column("id", ID_COLUMN_TYPE, primary_key=True),
    deepcopy(PROJECT_ID_COLUMN_REFERENCE),
    Column("type", String(get_enum_length(ObjectType)), nullable=False),
)


class DbIdsCounterModel(IdsCounterModel, DbModel):
    def get_new_id(self, project_id: str) -> ObjectId:
        query = select(
            [IDS_COUNTER_TABLE.c.next_id],
            for_update=True
        ).where(
            IDS_COUNTER_TABLE.c.project_id == project_id
        )
        result = self._session.execute(query).fetchone()
        if result:
            current_id = result["next_id"]
            query = update(IDS_COUNTER_TABLE).values(
                next_id=current_id + 1
            ).where(
                IDS_COUNTER_TABLE.c.project_id == project_id
            )
        else:
            current_id = 1
            query = insert(IDS_COUNTER_TABLE).values(
                project_id=project_id,
                next_id=current_id + 1
            )
        self._session.execute(query)
        mark_changed(self._session)
        return ObjectId.from_parts(project_id, current_id)


class DbObjectsTrackerModel(ObjectsTrackerModel, DbModel):
    def track_object(self, object_id: ObjectId, object_type: ObjectType):
        query = insert(OBJECTS_TRACKER_TABLE).values(
            id=object_id.object_id,
            project_id=object_id.project_id,
            type=object_type.value,
        )
        self._session.execute(query)
        mark_changed(self._session)

    def untrack_object(self, object_id: ObjectType):
        query = delete(OBJECTS_TRACKER_TABLE)
        query = query.where(OBJECTS_TRACKER_TABLE.c.id == object_id.object_id)
        self._session.execute(query)
        mark_changed(self._session)

    def get_objects_types(self, object_ids: List[ObjectId]) -> Dict[ObjectId, ObjectType]:
        query = select([OBJECTS_TRACKER_TABLE.c.id, OBJECTS_TRACKER_TABLE.c.type])
        query = query.where(
            OBJECTS_TRACKER_TABLE.c.id.in_(
                [object_id.object_id for object_id in object_ids]
            )
        )
        result = self._session.execute(query).fetchall()
        object_ids_map = {
            ObjectId(row["id"]): ObjectType(row["type"])
            for row
            in result
        }
        missing_ids = set(object_ids) - set(object_ids_map.keys())
        if missing_ids:
            raise ObjectsDoesNotExist(list(missing_ids))

        return object_ids_map

    def get_object_type(self, object_id: ObjectId) -> ObjectType:
        types_map = self.get_objects_types([object_id])
        return types_map[object_id]
