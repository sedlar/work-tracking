from datetime import datetime

import pytest

from tests.integration.factories.objs import create_bound_issue, create_project
from wt.entities.issues import IssueStatus, IssueDoesNotExist, IssuePriority, IssueType
from wt.ids import EntityId
from tests.integration.factories.objs import create_task, create_tag, create_file, create_link


def test_create_issue(issues_model, put_project):
    put_project(create_project())

    issue = create_bound_issue()
    issues_model.put_issue(issue)
    saved_issue = issues_model.get_issue(issue.object_id)
    assert issue == saved_issue


def test_update_issue(issues_model, put_project):
    put_project(create_project())

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
        files=[create_file("file_A"), create_file("file_B")],
        links=[create_link("link_A"), create_link("link_B")],
        tasks=[create_task("task_A"), create_task("task_B")],
        tags=[create_tag("tag_A"), create_tag("tag_B")],
    )
    issues_model.put_issue(updated_issue)

    saved_issue = issues_model.get_issue(issue.object_id)
    assert updated_issue == saved_issue


def test_get_issues(issues_model, put_project):
    put_project(create_project())

    issue1 = create_bound_issue()
    issues_model.put_issue(issue1)

    issue2 = create_bound_issue(
        object_id=issue1.object_id.project_id + "-2",
        name="Other issue"
    )
    issues_model.put_issue(issue2)

    issues = issues_model.get_issues(
        EntityId(issue1.object_id.project_id),
        related_entity_id=None,
        offset=0,
        limit=2
    )
    assert issues == [issue1, issue2]


def test_get_issues_filter_project(issues_model, put_project):
    put_project(create_project())
    put_project(create_project("AAA"))

    issue1 = create_bound_issue()
    issues_model.put_issue(issue1)

    issue2 = create_bound_issue(
        object_id="AAA",
        name="Other issue"
    )
    issues_model.put_issue(issue2)

    issues = issues_model.get_issues(
        EntityId(issue1.object_id.project_id),
        related_entity_id=None,
        offset=0,
        limit=2
    )
    assert issues == [issue1]


def test_delete_issue(issues_model, put_project):
    put_project(create_project())

    issue = create_bound_issue()
    issues_model.put_issue(issue)

    issues_model.delete_issue(issue.object_id)
    assert not issues_model.get_issues(
        EntityId(issue.object_id.project_id),
        related_entity_id=None,
        offset=0,
        limit=1
    )


def test_delete_issue_files(issues_model, put_project, files_model):
    put_project(create_project())

    issue = create_bound_issue()
    issues_model.put_issue(issue)

    issues_model.delete_issue(issue.object_id)
    assert not files_model.get_entity_files(issue.object_id)


def test_delete_issue_links(issues_model, put_project, links_model):
    put_project(create_project())

    issue = create_bound_issue()
    issues_model.put_issue(issue)

    issues_model.delete_issue(issue.object_id)
    assert not links_model.get_entity_links(issue.object_id)


def test_delete_issue_tags(issues_model, put_project, tags_model):
    put_project(create_project())

    issue = create_bound_issue()
    issues_model.put_issue(issue)

    issues_model.delete_issue(issue.object_id)
    assert not tags_model.get_entity_tags(issue.object_id)


def test_delete_issue_tasks(issues_model, put_project, tasks_model):
    put_project(create_project())

    issue = create_bound_issue()
    issues_model.put_issue(issue)

    issues_model.delete_issue(issue.object_id)
    assert not tasks_model.get_entity_tasks(issue.object_id)


def test_get_no_issue(issues_model):
    with pytest.raises(IssueDoesNotExist):
        issues_model.get_issue(EntityId("ABC-2"))


def test_delete_no_issue(issues_model):
    with pytest.raises(IssueDoesNotExist):
        issues_model.delete_issue(EntityId("ABC-2"))
