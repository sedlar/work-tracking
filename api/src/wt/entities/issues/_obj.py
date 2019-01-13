from datetime import datetime
from enum import Enum
from typing import List, Optional
from decimal import Decimal

from wt.ids import EntityId
from wt.fields.files import File
from wt.common import Money
from wt.fields.links import Link
from wt.fields.tags import Tag
from wt.fields.tasks import Task


class IssueStatus(Enum):
    new = "new"
    open = "open"
    review = "review"
    waiting = "waiting"
    done = "done"
    invalid = "invalid"
    duplicate = "duplicate"
    wontfix = "wontfix"
    archived = "archived"


class IssuePriority(Enum):
    blocker = "blocker"
    critical = "critical"
    major = "major"
    minor = "minor"
    trivial = "trivial"


class IssueType(Enum):
    task = "task"
    improvement = "improvement"
    feature = "feature"
    bug = "bug"
    education = "education"


class Issue:
    # pylint: disable=too-many-instance-attributes
    def __init__(
            self,
            name: str,
            status: IssueStatus,
            type_: IssueType,
            priority: IssuePriority,
            description: str,
            date_opened: datetime,
            date_closed: datetime,
            deadline: datetime,
            hour_rate: Optional[Money],
            estimated_duration: Optional[Decimal],
            external_type: str,
            files: List[File],
            links: List[Link],
            tags: List[Tag],
            tasks: List[Task],
    ):
        # pylint: disable=too-many-arguments,too-many-locals
        self.name = name
        self.status = status
        self.description = description
        self.date_opened = date_opened
        self.date_closed = date_closed
        self.deadline = deadline
        self.type = type_
        self.priority = priority
        self.hour_rate = hour_rate
        self.estimated_duration = estimated_duration
        self.external_type = external_type
        self.files = files
        self.links = links
        self.tags = tags
        self.tasks = tasks

    def __eq__(self, other):
        if isinstance(other, Issue):
            return self.__dict__ == other.__dict__

        return NotImplemented


class BoundIssue(Issue):
    def __init__(self, object_id: EntityId, issue):
        self.object_id = object_id
        super().__init__(
            name=issue.name,
            status=issue.status,
            description=issue.description,
            date_opened=issue.date_opened,
            date_closed=issue.date_closed,
            deadline=issue.deadline,
            external_type=issue.external_type,
            estimated_duration=issue.estimated_duration,
            hour_rate=issue.hour_rate,
            type_=issue.type,
            priority=issue.priority,
            files=issue.files,
            links=issue.links,
            tags=issue.tags,
            tasks=issue.tasks,
        )
