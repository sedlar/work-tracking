from typing import List

from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    select,
    UniqueConstraint,
    and_,
    delete,
    insert,
)
from zope.sqlalchemy import mark_changed

from wt.files import File, FilesModel
from wt.provider.db import METADATA, DbModel
from wt.provider.db.models.ids import ID_COLUMN_TYPE

FILES_TABLE = Table(
    "files",
    METADATA,
    Column("id", Integer(), primary_key=True, autoincrement=True),
    Column("parent_id", ID_COLUMN_TYPE),
    Column("uri", String(64)),
    UniqueConstraint("parent_id", "uri")
)


class DbFilesModel(FilesModel, DbModel):
    def set_object_files(self, object_id: str, files: List[File]):
        actual_uris = {file.uri for file in files}

        existing_uris = set(self._get_object_file_uris(object_id))

        added_uris = actual_uris - existing_uris
        removed_uris = existing_uris - actual_uris
        if added_uris:
            self._add_files(object_id, added_uris)

        if removed_uris:
            self._remove_files(object_id, removed_uris)

    def get_object_files(self, object_id: str):
        uris = self._get_object_file_uris(object_id)
        return [File(uri) for uri in uris]

    def _remove_files(self, object_id, removed_uris):
        remove_query = delete(FILES_TABLE).where(
            and_(
                FILES_TABLE.c.parent_id == object_id,
                FILES_TABLE.c.uri.in_(removed_uris)
            )
        )
        self._session.execute(remove_query)
        mark_changed(self._session)

    def _add_files(self, object_id, added_uris):
        add_query = insert(FILES_TABLE).values(
            [
                {
                    "parent_id": object_id,
                    "uri": uri
                }
                for uri
                in added_uris
            ]
        )
        self._session.execute(add_query)
        mark_changed(self._session)

    def _get_object_file_uris(self, object_id: str) -> List[str]:
        query = select([FILES_TABLE.c.uri]).where(FILES_TABLE.c.parent_id == object_id)
        query = query.order_by(FILES_TABLE.c.uri)
        rows = self._session.execute(query).fetchall()
        return [row["uri"] for row in rows]
