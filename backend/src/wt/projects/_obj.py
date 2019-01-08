from datetime import datetime
from enum import Enum
from typing import List

from wt.files import File
from wt.common import Money


class ProjectStatus(Enum):
    pending = "pending"
    open = "open"
    completed = "completed"
    archived = "archived"


class Project:
    # pylint: disable=too-many-instance-attributes
    def __init__(
            self,
            project_id: str,
            name: str,
            status: ProjectStatus,
            description: str,
            limitations_and_restrictions: str,
            goals_and_metrics: str,
            hour_rate: Money,
            primary_color: str,
            secondary_color: str,
            files: List[File],
            date_opened: datetime,
            date_closed: datetime,
            deadline: datetime,
    ):
        # pylint: disable=too-many-arguments
        self.project_id = project_id
        self.name = name
        self.status = status
        self.description = description
        self.limitations_and_restrictions = limitations_and_restrictions
        self.goals_and_metrics = goals_and_metrics
        self.hour_rate = hour_rate
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.files = files
        self.date_opened = date_opened
        self.date_closed = date_closed
        self.deadline = deadline

    def __eq__(self, other):
        if isinstance(other, Project):
            return self.__dict__ == other.__dict__

        return NotImplemented
