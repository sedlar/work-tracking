from typing import List, Optional
from wt.ids import EntityId, EntityType

from wt.entities.issues._model import IssuesModel
from wt.entities.issues._obj import Issue, BoundIssue
from wt.entities.issues._errors import IssueDoesNotExist
from wt.ids import IdsCounterModel, ObjectsTrackerModel
from wt.links import EntityLinksModel
from wt.costs.timesheets import TimesheetsModel
from wt.costs.expenditures import ExpendituresModel


class IssuesApi:
    def __init__(
            self,
            issues_model: IssuesModel,
            ids_counter_model: IdsCounterModel,
            objects_tracker_model: ObjectsTrackerModel,
            entity_links_model: EntityLinksModel,
            timesheets_model: TimesheetsModel,
            expenditures_model: ExpendituresModel,
    ):
        # pylint: disable=too-many-arguments
        self._issue_model = issues_model
        self._ids_counter_model = ids_counter_model
        self._objects_tracker_model = objects_tracker_model
        self._entity_links_model = entity_links_model
        self._timesheets_model = timesheets_model
        self._expenditures_model = expenditures_model

    def create_issue(
            self,
            project_id: EntityId,
            issue: Issue
    ) -> BoundIssue:
        issue_id = self._ids_counter_model.get_new_id(project_id)
        bound_issue = BoundIssue(issue_id, issue)
        self._issue_model.put_issue(bound_issue)
        self._objects_tracker_model.track_object(issue_id, EntityType.issue)
        return bound_issue

    def edit_issue(self, issue: BoundIssue):
        object_type = self._objects_tracker_model.get_object_type(issue.object_id)
        if object_type != EntityType.issue:
            raise IssueDoesNotExist(issue.object_id)
        self._issue_model.put_issue(issue)

    def get_issue(self, issue_id: EntityId) -> BoundIssue:
        return self._issue_model.get_issue(issue_id)

    def get_issues(
            self,
            project_id: EntityId,
            related_entity_id: Optional[EntityId],
            offset: int,
            limit: int
    ) -> List[BoundIssue]:
        return self._issue_model.get_issues(project_id, related_entity_id, offset, limit)

    def delete_issue(self, issue_id: EntityId):
        self._timesheets_model.delete_entity_timesheets(issue_id)
        self._expenditures_model.delete_entity_expenditures(issue_id)
        self._entity_links_model.delete_links(issue_id)
        self._issue_model.delete_issue(issue_id)
        self._objects_tracker_model.untrack_object(issue_id)
