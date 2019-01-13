from collections import Counter
from datetime import datetime
from typing import List, Set

from sqlalchemy import (
    select,
    and_,
    insert,
    delete,
)
from zope.sqlalchemy import mark_changed

from wt.fields.files import DuplicateFileReceived
from wt.fields.files import File, FilesModel
from wt.fields.links import Link, LinksModel, DuplicateLinkReceived
from wt.provider.db import DbModel
from wt.provider.db.tables import FILES_TABLE, LINKS_TABLE, TAGS_TABLE, TASKS_TABLE
from wt.fields.tags import Tag, DuplicateTagReceived, TagsModel
from wt.fields.tasks import Task, DuplicateTaskReceived, TasksModel
from wt.fields import FieldItem
from wt.ids import EntityId


class DbListFieldsModel(DbModel):
    duplicate_exception = Exception
    table = None
    id_column = None

    def _set_object_field_items(self, entity_id, items):
        actual_ids = {self._get_item_unique_id(item) for item in items}

        if len(actual_ids) < len(items):
            counter = Counter(self._get_item_unique_id(item) for item in items)
            raise self.duplicate_exception(
                [
                    item_id for item_id, count in counter.items() if count > 1
                ]
            )

        existing_ids = set(
            self._get_item_unique_id(item)
            for item
            in self._get_object_items(entity_id)
        )

        added_ids = actual_ids - existing_ids
        removed_ids = existing_ids - actual_ids

        added_items = [
            item
            for item
            in items if
            self._get_item_unique_id(item) in added_ids]

        if added_ids:
            self._add_items(entity_id, added_items)

        if removed_ids:
            self._remove_items(entity_id, removed_ids)

    def _add_items(self, entity_id: EntityId, items: List[FieldItem]):
        now = datetime.now()
        data = [self._item_to_dict(item) for item in items]
        for item in data:
            item["created_on"] = now
            item["parent_id"] = entity_id.full_id

        add_query = insert(self.table).values(data)
        self._session.execute(add_query)
        mark_changed(self._session)

    def _remove_items(self, entity_id: EntityId, removed_item_ids: Set[str]):
        remove_query = delete(self.table).where(
            and_(
                self.table.c.parent_id == entity_id.full_id,
                self.id_column.in_(removed_item_ids)
            )
        )
        self._session.execute(remove_query)
        mark_changed(self._session)

    def _get_object_items(self, entity_id):
        query = select([self.table]).where(self.table.c.parent_id == entity_id.full_id)
        query = query.order_by(self.id_column)
        return [
            self._row_to_item(row)
            for row
            in self._session.execute(query).fetchall()
        ]

    def _row_to_item(self, row):
        raise NotImplementedError()

    def _item_to_dict(self, item: FieldItem) -> dict:
        raise NotImplementedError()

    def _get_item_unique_id(self, item: FieldItem) -> str:
        raise NotImplementedError()


class DbTagsModel(DbListFieldsModel, TagsModel):
    duplicate_exception = DuplicateTagReceived
    table = TAGS_TABLE
    id_column = TAGS_TABLE.c.tag

    def set_entity_tags(self, entity_id: EntityId, tags: List[Tag]):
        self._set_object_field_items(entity_id, tags)

    def get_entity_tags(self, entity_id: EntityId) -> List[Tag]:
        return self._get_object_items(entity_id)

    def _get_item_unique_id(self, item: Tag):
        return item.tag

    def _row_to_item(self, row):
        return Tag(row["tag"])

    def _item_to_dict(self, item: Tag) -> dict:
        return {
            "tag": item.tag
        }


class DbFilesModel(FilesModel, DbListFieldsModel):
    duplicate_exception = DuplicateFileReceived
    table = FILES_TABLE
    id_column = FILES_TABLE.c.uri

    def set_entity_files(self, entity_id: EntityId, files: List[File]):
        self._set_object_field_items(entity_id, files)

    def get_entity_files(self, entity_id: EntityId):
        return self._get_object_items(entity_id)

    def _get_item_unique_id(self, item: File):
        return item.uri

    def _row_to_item(self, row):
        return File(row["uri"])

    def _item_to_dict(self, item: File) -> dict:
        return {
            "uri": item.uri,
        }


class DbLinksModel(LinksModel, DbListFieldsModel):
    duplicate_exception = DuplicateLinkReceived
    table = LINKS_TABLE
    id_column = LINKS_TABLE.c.uri

    def set_entity_links(self, entity_id: EntityId, links: List[Link]):
        self._set_object_field_items(entity_id, links)

    def get_entity_links(self, entity_id: EntityId):
        return self._get_object_items(entity_id)

    def _get_item_unique_id(self, item: Link):
        return item.uri

    def _row_to_item(self, row):
        return Link(
            uri=row["uri"],
            title=row["title"],
            description=row["description"],
        )

    def _item_to_dict(self, item: Link) -> dict:
        return {
            "uri": item.uri,
            "title": item.title,
            "description": item.description,
        }


class DbTasksModel(TasksModel, DbListFieldsModel):
    duplicate_exception = DuplicateTaskReceived
    table = TASKS_TABLE
    id_column = TASKS_TABLE.c.task

    def set_entity_tasks(self, entity_id: EntityId, tasks: List[Task]):
        self._set_object_field_items(entity_id, tasks)

    def get_entity_tasks(self, entity_id: EntityId) -> List[Task]:
        return self._get_object_items(entity_id)

    def _get_item_unique_id(self, item: Task):
        return item.task

    def _row_to_item(self, row):
        return Task(
            task=row["task"],
            completed=row["completed"],
        )

    def _item_to_dict(self, item: Task) -> dict:
        return {
            "task": item.task,
            "completed": item.completed,
        }
