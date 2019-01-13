from typing import List, Dict

from sqlalchemy import select, delete, update, insert
from zope.sqlalchemy import mark_changed

from wt.ids import (
    IdsCounterModel,
    EntityId,
    ObjectType,
    ObjectsTrackerModel,
)
from wt.provider.db import DbModel
from wt.provider.db.tables import IDS_COUNTER_TABLE, OBJECTS_TRACKER_TABLE


class DbIdsCounterModel(IdsCounterModel, DbModel):
    def get_new_id(self, project_id: EntityId) -> EntityId:
        query = select(
            [IDS_COUNTER_TABLE.c.next_id],
            for_update=True
        ).where(
            IDS_COUNTER_TABLE.c.project_id == project_id.project_id
        )
        result = self._session.execute(query).fetchone()
        if result:
            current_id = result["next_id"]
            query = update(IDS_COUNTER_TABLE).values(
                next_id=current_id + 1
            ).where(
                IDS_COUNTER_TABLE.c.project_id == project_id.project_id
            )
        else:
            current_id = 1
            query = insert(IDS_COUNTER_TABLE).values(
                project_id=project_id.project_id,
                next_id=current_id + 1
            )
        self._session.execute(query)
        mark_changed(self._session)
        return EntityId.from_parts(project_id.project_id, current_id)

    def drop_project(self, project_id: EntityId):
        query = delete(IDS_COUNTER_TABLE).where(
            IDS_COUNTER_TABLE.c.project_id == project_id.project_id
        )
        self._session.execute(query)
        mark_changed(self._session)


class DbObjectsTrackerModel(ObjectsTrackerModel, DbModel):
    def track_object(self, object_id: EntityId, object_type: ObjectType):
        query = insert(OBJECTS_TRACKER_TABLE).values(
            id=object_id.full_id,
            project_id=object_id.project_id,
            type=object_type.value,
        )
        self._session.execute(query)
        mark_changed(self._session)

    def untrack_object(self, object_id: EntityId):
        query = delete(OBJECTS_TRACKER_TABLE)
        query = query.where(OBJECTS_TRACKER_TABLE.c.id == object_id.full_id)
        self._session.execute(query)
        mark_changed(self._session)

    def get_objects_types(self, object_ids: List[EntityId]) -> Dict[EntityId, ObjectType]:
        query = select([OBJECTS_TRACKER_TABLE.c.id, OBJECTS_TRACKER_TABLE.c.type])
        query = query.where(
            OBJECTS_TRACKER_TABLE.c.id.in_(
                [object_id.full_id for object_id in object_ids]
            )
        )
        result = self._session.execute(query).fetchall()
        return self._result_to_map(result)

    def get_objects_types_by_project(self, project_id: EntityId) -> Dict[EntityId, ObjectType]:
        query = select([OBJECTS_TRACKER_TABLE.c.id, OBJECTS_TRACKER_TABLE.c.type])
        query = query.where(
            OBJECTS_TRACKER_TABLE.c.project_id == project_id.project_id,
        )
        query = query.where(
            OBJECTS_TRACKER_TABLE.c.type != ObjectType.project.value,
        )
        result = self._session.execute(query).fetchall()
        return self._result_to_map(result)

    @staticmethod
    def _result_to_map(result):
        return {
            EntityId(row["id"]): ObjectType(row["type"])
            for row
            in result
        }

    def get_object_type(self, object_id: EntityId) -> ObjectType:
        types_map = self.get_objects_types([object_id])

        return types_map.get(object_id)
