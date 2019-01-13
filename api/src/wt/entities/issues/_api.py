from typing import List
from wt.ids import EntityId, ObjectType

from wt.entities.issues._model import IssuesModel
from wt.entities.issues._obj import Issue, BoundIssue
from wt.entities.issues._errors import IssueDoesNotExist
from wt.ids import IdsCounterModel, ObjectsTrackerModel


class IssuesApi:
    def __init__(
            self,
            issues_model: IssuesModel,
            ids_counter_model: IdsCounterModel,
            objects_tracker_model: ObjectsTrackerModel
    ):
        self._issue_model = issues_model
        self._ids_counter_model = ids_counter_model
        self._objects_tracker_model = objects_tracker_model

    def create_issue(
            self,
            project_id: EntityId,
            issue: Issue
    ) -> BoundIssue:
        issue_id = self._ids_counter_model.get_new_id(project_id)
        bound_issue = BoundIssue(issue_id, issue)
        self._issue_model.put_issue(bound_issue)
        self._objects_tracker_model.track_object(issue_id, ObjectType.issue)
        return bound_issue

    def edit_issue(self, issue: BoundIssue):
        object_type = self._objects_tracker_model.get_object_type(issue.object_id)
        if object_type != ObjectType.issue:
            raise IssueDoesNotExist(issue.object_id)
        self._issue_model.put_issue(issue)

    def get_issue(self, issue_id: EntityId) -> BoundIssue:
        return self._issue_model.get_issue(issue_id)

    def get_issues(
            self,
            project_id: EntityId,
            offset: int,
            limit: int
    ) -> List[BoundIssue]:
        return self._issue_model.get_issues(project_id, offset, limit)

    def delete_issue(self, issue_id: EntityId):
        self._issue_model.delete_issue(issue_id)
        self._objects_tracker_model.untrack_object(issue_id)