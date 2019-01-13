from __future__ import annotations

from enum import Enum


class ObjectType(Enum):
    project = "project"
    deliverable = "deliverable"
    issue = "issue"
    design = "design"
    meeting = "meeting"


class EntityId:
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

    def __repr__(self):
        return self.full_id

    def __eq__(self, other):
        if isinstance(other, EntityId):
            return self.full_id == other.full_id
        return NotImplemented

    def __hash__(self):
        return hash(self.full_id)
