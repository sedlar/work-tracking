from typing import List

from wt.ids import EntityId
from wt.entities.issues._obj import BoundIssue


class IssuesModel:
    def put_issue(self, issue: BoundIssue):
        raise NotImplementedError()

    def get_issue(self, issue_id: EntityId) -> BoundIssue:
        raise NotImplementedError()

    def get_issues(self, project_id: EntityId, offset: int, limit: int) -> List[BoundIssue]:
        raise NotImplementedError()

    def delete_issue(self, issue_id: EntityId):
        raise NotImplementedError()
