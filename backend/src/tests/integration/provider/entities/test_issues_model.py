from datetime import datetime

import pytest

from tests.integration.factories.objs import create_bound_issue, create_project
from wt.entities.issues import IssueStatus, IssueDoesNotExist, IssuePriority, IssueType
from wt.ids import EntityId


def test_create_issue(issues_model, projects_model):
    projects_model.put_project(create_project())

    issue = create_bound_issue()
    issues_model.put_issue(issue)
    saved_issue = issues_model.get_issue(issue.object_id)
    assert issue == saved_issue


def test_update_issue(issues_model, projects_model):
    projects_model.put_project(create_project())

    issue = create_bound_issue()
    issues_model.put_issue(issue)

    updated_issue = create_bound_issue(
        name="Test",
        status=IssueStatus.done,
        type=IssueType.task,
        priority=IssuePriority.major,
        description="DESC",
        date_opened=datetime(year=2020, month=1, day=1, hour=10, minute=30),
        date_closed=datetime(year=2020, month=1, day=2, hour=10, minute=30),
        deadline=datetime(year=2020, month=1, day=3, hour=10, minute=30),
        files=[],
        links=[],
        tasks=[],
        tags=[],
    )
    issues_model.put_issue(updated_issue)

    saved_issue = issues_model.get_issue(issue.object_id)
    assert updated_issue == saved_issue


def test_get_issues(issues_model, projects_model):
    projects_model.put_project(create_project())

    issue1 = create_bound_issue()
    issues_model.put_issue(issue1)

    issue2 = create_bound_issue(
        object_id=issue1.object_id.project_id + "-2",
        name="Other issue"
    )
    issues_model.put_issue(issue2)

    issues = issues_model.get_issues(EntityId(issue1.object_id.project_id), 0, 2)
    assert issues == [issue1, issue2]


def test_get_issues_filter_project(issues_model, projects_model):
    projects_model.put_project(create_project())
    projects_model.put_project(create_project("AAA"))

    issue1 = create_bound_issue()
    issues_model.put_issue(issue1)

    issue2 = create_bound_issue(
        object_id="AAA",
        name="Other issue"
    )
    issues_model.put_issue(issue2)

    issues = issues_model.get_issues(
        EntityId(issue1.object_id.project_id),
        0,
        2
    )
    assert issues == [issue1]


def test_delete_issue(issues_model, projects_model):
    projects_model.put_project(create_project())

    issue = create_bound_issue()
    issues_model.put_issue(issue)

    issues_model.delete_issue(issue.object_id)
    assert not issues_model.get_issues(EntityId(issue.object_id.project_id), 0, 1)


def test_get_no_issue(issues_model):
    with pytest.raises(IssueDoesNotExist):
        issues_model.get_issue(EntityId("ABC-2"))


def test_delete_no_issue(issues_model):
    with pytest.raises(IssueDoesNotExist):
        issues_model.delete_issue(EntityId("ABC-2"))
