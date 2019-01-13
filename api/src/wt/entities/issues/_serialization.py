from typing import List

from wt.common.serializers import (
    remove_nones,
    serialize_datetime,
    deserialize_datetime,
    deserialize_money,
    serialize_money,
)
from wt.entities.issues._obj import Issue, BoundIssue, IssueStatus, IssuePriority, IssueType
from wt.fields.files import FileSerializer, FileDeserializer
from wt.fields.links import LinkSerializer, LinkDeserializer
from wt.fields.tags import TagSerializer, TagDeserializer
from wt.fields.tasks import TaskSerializer, TaskDeserializer
from wt.ids import EntityId


class IssueSerializer:
    def __init__(
            self,
            files_serializer: FileSerializer,
            links_serializer: LinkSerializer,
            tags_serializer: TagSerializer,
            tasks_serializer: TaskSerializer,
    ):
        self._files_serializer = files_serializer
        self._links_serializer = links_serializer
        self._tags_serializer = tags_serializer
        self._tasks_serializer = tasks_serializer

    def serialize_issue(self, issue: BoundIssue) -> dict:
        return remove_nones(
            {
                "id": issue.object_id.full_id,
                "name": issue.name,
                "status": issue.status.value,
                "type": issue.type.value,
                "priority": issue.priority.value,
                "date_opened": serialize_datetime(issue.date_opened),
                "date_closed": serialize_datetime(issue.date_closed),
                "deadline": serialize_datetime(issue.deadline),
                "description": issue.description,
                "external_type": issue.external_type,
                "estimated_duration": issue.estimated_duration,
                "files": self._files_serializer.serialize_files(issue.files),
                "links": self._links_serializer.serialize_links(issue.links),
                "tags": self._tags_serializer.serialize_tags(issue.tags),
                "tasks": self._tasks_serializer.serialize_tasks(issue.tasks),
                "hour_rate": serialize_money(issue.hour_rate) if issue.hour_rate else None,
            }
        )

    def serialize_issues(self, issues: List[BoundIssue]) -> List[dict]:
        return [
            self.serialize_issue(issue)
            for issue
            in issues
        ]


class IssueDeserializer:
    def __init__(
            self,
            files_deserializer: FileDeserializer,
            links_deserializer: LinkDeserializer,
            tags_deserializer: TagDeserializer,
            tasks_deserializer: TaskDeserializer,
    ):
        self._files_deserializer = files_deserializer
        self._links_deserializer = links_deserializer
        self._tags_deserializer = tags_deserializer
        self._tasks_deserializer = tasks_deserializer

    def deserialize_issue(self, issue: dict) -> Issue:
        return Issue(
            name=issue["name"],
            status=IssueStatus(issue["status"]),
            priority=IssuePriority(issue["priority"]),
            type_=IssueType(issue["type"]),
            date_opened=deserialize_datetime(issue["date_opened"]),
            date_closed=deserialize_datetime(issue.get("date_closed")),
            deadline=deserialize_datetime(issue.get("deadline")),
            description=issue["description"],
            external_type=issue["external_type"],
            estimated_duration=issue.get("estimated_duration"),
            files=self._files_deserializer.deserialize_files(issue["files"]),
            links=self._links_deserializer.deserialize_links(issue["links"]),
            tags=self._tags_deserializer.deserialize_tags(issue["tags"]),
            tasks=self._tasks_deserializer.deserialize_tasks(issue["tasks"]),
            hour_rate=deserialize_money(issue["hour_rate"]) if "hour_rate" in issue else None,
        )

    def deserialize_bound_issue(
            self,
            issue_id: str,
            issue: dict
    ) -> BoundIssue:
        return BoundIssue(
            object_id=EntityId(issue_id),
            issue=self.deserialize_issue(issue)
        )
