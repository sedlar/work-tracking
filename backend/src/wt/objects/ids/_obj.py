from __future__ import annotations

from enum import Enum


class ObjectType(Enum):
    deliverable = "deliverable"
    issue = "issue"
    design = "design"
    meeting = "meeting"


class ObjectId:
    def __init__(self, object_id: str):
        self.object_id = object_id

    @classmethod
    def from_parts(cls, project_id: str, object_id: int) -> ObjectId:
        return cls(
            "{project_id}-{object_id}".format(
                project_id=project_id,
                object_id=object_id,
            )
        )

    @property
    def project_id(self) -> str:
        return self.object_id.split("-")[0]

    def __eq__(self, other):
        if isinstance(other, ObjectId):
            return self.object_id == other.object_id
        return NotImplemented

    def __hash__(self):
        return hash(self.object_id)
