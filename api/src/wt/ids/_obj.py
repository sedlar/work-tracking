from __future__ import annotations

from enum import Enum


class EntityType(Enum):
    project = "project"
    deliverable = "deliverable"
    issue = "issue"
    design = "design"
    meeting = "meeting"


class SimpleEntityType(Enum):
    timesheet = "ts"
    expenditure = "ex"


class BaseId:
    full_id = None

    def __repr__(self):
        return self.full_id

    def __eq__(self, other):
        if isinstance(other, BaseId):
            return self.full_id == other.full_id
        return NotImplemented

    def __hash__(self):
        return hash(self.full_id)


class EntityId(BaseId):
    def __init__(self, full_id: str):
        self.full_id = full_id
        if "-" in full_id:
            self.project_id = self.full_id.split("-")[0]
        else:
            self.project_id = self.full_id

    @classmethod
    def from_parts(cls, project_id: str, object_id: int) -> EntityId:
        return cls(
            "{project_id}-{object_id}".format(
                project_id=project_id,
                object_id=object_id,
            )
        )


class SimpleId(BaseId):
    def __init__(self, object_type: SimpleEntityType, simple_id: int):
        self.object_type = object_type
        self.simple_id = simple_id

    @property
    def full_id(self):
        return "{object_type}-{id}".format(
            object_type=self.object_type.value,
            id=self.simple_id,
        )
