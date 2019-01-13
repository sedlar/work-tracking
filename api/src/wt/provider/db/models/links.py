from sqlalchemy import delete, or_, and_
from sqlalchemy.dialects.postgresql import insert
from zope.sqlalchemy import mark_changed

from wt.ids import EntityId
from wt.links import EntityLinksModel, LinkDoesNotExist, LinkAlreadyExists
from wt.provider.db import DbModel
from wt.provider.db.tables import ENTITY_LINKS_TABLE


class DbEntityLinksModel(EntityLinksModel, DbModel):
    def create_link(self, entity_id: EntityId, other_entity_id: EntityId):
        data = [
            {
                "object_id": entity_id.full_id,
                "other_object_id": other_entity_id.full_id,
            },
            {
                "object_id": other_entity_id.full_id,
                "other_object_id": entity_id.full_id,
            },
        ]
        query = insert(ENTITY_LINKS_TABLE).values(data).on_conflict_do_nothing()
        result = self._session.execute(query)
        if result.rowcount == 0:
            raise LinkAlreadyExists()
        mark_changed(self._session)

    def delete_link(self, entity_id: EntityId, other_entity_id: EntityId):
        query = delete(ENTITY_LINKS_TABLE).where(
            or_(
                and_(
                    ENTITY_LINKS_TABLE.c.object_id == entity_id.full_id,
                    ENTITY_LINKS_TABLE.c.other_object_id == other_entity_id.full_id,
                ),
                and_(
                    ENTITY_LINKS_TABLE.c.object_id == other_entity_id.full_id,
                    ENTITY_LINKS_TABLE.c.other_object_id == entity_id.full_id,
                    ),
            )
        )
        result = self._session.execute(query)
        if result.rowcount == 0:
            raise LinkDoesNotExist()
        mark_changed(self._session)

    def delete_links(self, entity_id: EntityId):
        query = delete(ENTITY_LINKS_TABLE).where(
            or_(
                ENTITY_LINKS_TABLE.c.object_id == entity_id.full_id,
                ENTITY_LINKS_TABLE.c.other_object_id == entity_id.full_id,
            )
        )
        self._session.execute(query)
        mark_changed(self._session)
