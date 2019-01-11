from collections import Counter
from datetime import datetime
from typing import List

from sqlalchemy import (
    select,
    and_,
    insert,
    delete,
)
from zope.sqlalchemy import mark_changed

from wt.fields.files import DuplicateFileReceived
from wt.fields.files import File, FilesModel
from wt.fields.links import Link, LinksModel, DuplicateLinkSent
from wt.provider.db import DbModel
from wt.provider.db.tables import FILES_TABLE
from wt.provider.db.tables import LINKS_TABLE


class DbFilesModel(FilesModel, DbModel):
    def set_object_files(self, object_id: str, files: List[File]):
        actual_uris = {file.uri for file in files}
        if len(actual_uris) < len(files):
            counter = Counter(file.uri for file in files)
            raise DuplicateFileReceived([uri for uri, count in counter.items() if count > 1])

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
        now = datetime.now()
        add_query = insert(FILES_TABLE).values(
            [
                {
                    "parent_id": object_id,
                    "uri": uri,
                    "created_on": now,
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


class DbLinksModel(LinksModel, DbModel):
    def set_object_links(self, object_id: str, links: List[Link]):
        actual_uris = {link.uri for link in links}
        if len(actual_uris) < len(links):
            counter = Counter(link.uri for link in links)
            raise DuplicateLinkSent([uri for uri, count in counter.items() if count > 1])

        existing_links = self._get_object_links_rows(object_id)
        existing_link_uris = set(link.uri for link in existing_links)

        added_uris = actual_uris - existing_link_uris
        removed_uris = existing_link_uris - actual_uris
        if added_uris:
            self._add_links(object_id, [link for link in links if link.uri in added_uris])

        if removed_uris:
            self._remove_links(object_id, removed_uris)

    def get_object_links(self, object_id: str):
        rows = self._get_object_links_rows(object_id)
        return [Link(uri=row.uri, name=row.name, description=row.description) for row in rows]

    def _remove_links(self, object_id, removed_uris):
        remove_query = delete(LINKS_TABLE).where(
            and_(
                LINKS_TABLE.c.parent_id == object_id,
                LINKS_TABLE.c.uri.in_(removed_uris)
            )
        )
        self._session.execute(remove_query)
        mark_changed(self._session)

    def _add_links(self, object_id, added_links):
        now = datetime.now()
        add_query = insert(LINKS_TABLE).values(
            [
                {
                    "parent_id": object_id,
                    "uri": link.uri,
                    "name": link.name,
                    "description": link.description,
                    "created_on": now,
                }
                for link
                in added_links
            ]
        )
        self._session.execute(add_query)
        mark_changed(self._session)

    def _get_object_links_rows(self, object_id: str):
        query = select([LINKS_TABLE]).where(LINKS_TABLE.c.parent_id == object_id)
        query = query.order_by(LINKS_TABLE.c.uri)
        return self._session.execute(query).fetchall()
