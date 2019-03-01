from typing import Union

import pytest

from tests.integration.factories.objs import (
    create_project,
    create_issue,
    create_money,
    create_deliverable,
    create_timesheet,
    create_expenditure,
)
from tests.integration.http.conftest import MINIMAL_EMPTY_STATS, FULL_EMPTY_STATS
from tests.integration.http.test_projects import BASE_PROJECTS_URL
from wt.entities.issues import BoundIssue
from wt.entities.issues import IssueDoesNotExist, IssueStatus, IssueType, IssuePriority
from wt.ids import EntityId

BASE_ISSUES_URL = "/issues"

MINIMAL_SERIALIZED_ISSUE = {
    "date_opened": "2019-01-01T10:30:05",
    "description": "Description issue",
    "name": "Dummy issue",
    "files": [],
    "links": [],
    "tags": [],
    "tasks": [],
    "external_type": "",
    "status": "new",
    "priority": "minor",
    "type": "task",
}
FULL_SERIALIZED_ISSUE = {
    "date_opened": "2019-01-01T10:30:05",
    "date_closed": "2019-01-02T10:30:05",
    "deadline": "2019-01-03T10:30:05",
    "description": "Description issue",
    "external_type": "external_type",
    "name": "Dummy issue",
    "status": "open",
    "priority": "critical",
    "type": "bug",
    "files": ["File1", "File2"],
    "links": [
        {
            "uri": "www.google.com",
            "title": "Google",
            "description": "Google link",
        },
        {
            "uri": "www.zoho.cz",
            "title": "zoho",
            "description": "zoho",
        },
    ],
    "tags": ["X", "Y"],
    "tasks": [
        {
            "task": "Implement work tracking api",
            "completed": False
        },
        {
            "task": "Task",
            "completed": True
        },
    ],
    "hour_rate": {
        "amount": 600.5,
        "currency": "CZK"
    },
    "estimated_duration": 10,
}

MINIMAL_ISSUE = create_issue(
    date_closed=None,
    deadline=None,
    estimated_duration=None,
    hour_rate=None,
    files=[],
    links=[],
    tags=[],
    tasks=[],
    status=IssueStatus.new,
    type=IssueType.task,
    priority=IssuePriority.minor,
    external_type="",
)
FULL_ISSUE = create_issue(
    hour_rate=create_money()
)


def get_project_issues_url(project_id: Union[str, EntityId]):
    return "{base_project}/{project_id}{base}".format(
        project_id=project_id,
        base=BASE_ISSUES_URL,
        base_project=BASE_PROJECTS_URL,
    )


def get_issue_url(issue_id: Union[str, EntityId]):
    return "{base}/{issue_id}".format(
        issue_id=issue_id,
        base=BASE_ISSUES_URL,
    )


@pytest.mark.parametrize(
    "serialized_issue,issue",
    [
        [
            FULL_SERIALIZED_ISSUE, FULL_ISSUE,
        ],
        [
            MINIMAL_SERIALIZED_ISSUE, MINIMAL_ISSUE,
        ],
    ]
)
def test_post_issue(
        authorized_api_request,
        get_issue,
        serialized_issue,
        issue,
        put_project,
):
    put_project(create_project())

    response = authorized_api_request(
        "POST",
        get_project_issues_url("PRJ"),
        {"issue": serialized_issue}
    )
    assert response.status_code == 201

    loaded_issue = get_issue(EntityId(response.json["id"]))
    assert loaded_issue.__dict__ == BoundIssue(
        EntityId("PRJ-1"),
        issue
    ).__dict__


def test_post_existing_issue(authorized_api_request, get_issue, put_project):
    put_project(create_project())

    authorized_api_request(
        "POST",
        get_project_issues_url("PRJ"),
        {"issue": MINIMAL_SERIALIZED_ISSUE}
    )
    response = authorized_api_request(
        "POST",
        get_project_issues_url("PRJ"),
        {"issue": FULL_SERIALIZED_ISSUE}
    )
    assert response.status_code == 201

    loaded_issue = get_issue(EntityId(response.json["id"]))
    assert loaded_issue.__dict__ == BoundIssue(
        EntityId("PRJ-2"),
        FULL_ISSUE
    ).__dict__


def test_put_issue(authorized_api_request, get_issue, put_project):
    put_project(create_project())

    response = authorized_api_request(
        "POST",
        get_project_issues_url("PRJ"),
        {"issue": MINIMAL_SERIALIZED_ISSUE}
    )
    issue_id = EntityId(response.json["id"])
    response = authorized_api_request(
        "PUT",
        get_issue_url(str(issue_id)),
        {"issue": FULL_SERIALIZED_ISSUE}
    )
    assert response.status_code == 200

    loaded_issue = get_issue(issue_id)
    assert loaded_issue.__dict__ == BoundIssue(
        issue_id,
        FULL_ISSUE
    ).__dict__


def test_put_missing_issue(authorized_api_request):
    response = authorized_api_request(
        "PUT",
        get_issue_url("AAA-3"),
        {"issue": FULL_SERIALIZED_ISSUE}
    )
    assert response.status_code == 404


def test_get_missing_issue(authorized_api_request):
    response = authorized_api_request("GET", get_issue_url("AAA-3"))
    assert response.status_code == 404


@pytest.mark.parametrize(
    "issue,serialized_issue,serialized_stats",
    [
        [FULL_ISSUE, FULL_SERIALIZED_ISSUE, FULL_EMPTY_STATS],
        [MINIMAL_ISSUE, MINIMAL_SERIALIZED_ISSUE, MINIMAL_EMPTY_STATS],
    ]
)
def test_get_issue(
        authorized_api_request,
        post_issue,
        issue,
        serialized_issue,
        serialized_stats,
        put_project,
):
    project = create_project()
    put_project(project)
    bound_issue = post_issue(project.project_id, issue)

    response = authorized_api_request(
        "GET",
        get_issue_url(str(bound_issue.object_id))
    )

    assert response.status_code == 200
    assert response.json["issue"]["id"] == str(bound_issue.object_id)

    del response.json["issue"]["id"]
    assert response.json == {
        "issue": serialized_issue,
        "stats": serialized_stats,
    }


@pytest.mark.parametrize(
    "url",
    (
            get_project_issues_url(create_project().project_id),
            BASE_ISSUES_URL,
    )
)
def test_get_issues(authorized_api_request, post_issue, put_project, url):
    project = create_project()
    put_project(project)
    minimal_bound_issue = post_issue(project.project_id, MINIMAL_ISSUE)
    full_bound_issue = post_issue(project.project_id, FULL_ISSUE)

    response = authorized_api_request("GET", url)

    assert response.status_code == 200
    assert response.json["issues"][0]["id"] == str(minimal_bound_issue.object_id)
    assert response.json["issues"][1]["id"] == str(full_bound_issue.object_id)
    del response.json["issues"][0]["id"]
    del response.json["issues"][1]["id"]
    assert response.json == {
        "issues":
        [
            MINIMAL_SERIALIZED_ISSUE,
            FULL_SERIALIZED_ISSUE
        ]
    }


@pytest.mark.parametrize(
    "url",
    (
            get_project_issues_url(create_project().project_id),
            BASE_ISSUES_URL,
    )
)
def test_get_issues_limit(authorized_api_request, post_issue, put_project, url):
    project = create_project()
    put_project(project)
    minimal_bound_issue = post_issue(project.project_id, MINIMAL_ISSUE)
    post_issue(project.project_id, FULL_ISSUE)

    response = authorized_api_request(
        "GET",
        url + "?limit=1"
    )

    assert response.status_code == 200
    assert response.json["issues"][0]["id"] == str(minimal_bound_issue.object_id)
    del response.json["issues"][0]["id"]
    assert response.json == {"issues": [MINIMAL_SERIALIZED_ISSUE]}


@pytest.mark.parametrize(
    "url",
    (
            get_project_issues_url(create_project().project_id),
            BASE_ISSUES_URL,
    )
)
def test_get_issues_offset(authorized_api_request, post_issue, put_project, url):
    project = create_project()
    put_project(project)
    post_issue(project.project_id, MINIMAL_ISSUE)
    full_bound_issue = post_issue(project.project_id, FULL_ISSUE)

    response = authorized_api_request(
        "GET",
        url + "?offset=1"
    )

    assert response.status_code == 200
    assert response.json["issues"][0]["id"] == str(full_bound_issue.object_id)
    del response.json["issues"][0]["id"]
    assert response.json == {"issues": [FULL_SERIALIZED_ISSUE]}


def test_get_issues_filter_related_object(
        authorized_api_request,
        post_issue,
        put_project,
        post_deliverable,
        put_link
):
    project = create_project()
    put_project(project)
    post_issue(project.project_id, MINIMAL_ISSUE)
    full_bound_issue = post_issue(project.project_id, FULL_ISSUE)
    deliverable = post_deliverable(project.project_id, create_deliverable())
    put_link(deliverable.object_id, full_bound_issue.object_id)

    response = authorized_api_request(
        "GET",
        get_project_issues_url(project.project_id) + "?related_object_id={id}".format(
            id=deliverable.object_id.full_id
        )
    )

    assert response.status_code == 200
    assert response.json["issues"][0]["id"] == str(full_bound_issue.object_id)
    del response.json["issues"][0]["id"]
    assert response.json == {"issues": [FULL_SERIALIZED_ISSUE]}


def test_delete_issue(authorized_api_request, post_issue, get_issue, put_project):
    project = create_project()
    put_project(project)
    issue = create_issue()
    bound_issue = post_issue(project.project_id, issue)

    authorized_api_request("DELETE", get_issue_url(str(bound_issue.object_id)))

    with pytest.raises(IssueDoesNotExist):
        get_issue(bound_issue.object_id)


def test_delete_issue_with_links(authorized_api_request, post_issue, get_issue, put_project, put_link):
    project = create_project()
    put_project(project)
    bound_issue1 = post_issue(project.project_id, create_issue())
    bound_issue2 = post_issue(project.project_id, create_issue())
    put_link(bound_issue1.object_id, bound_issue2.object_id)

    authorized_api_request("DELETE", get_issue_url(str(bound_issue1.object_id)))

    with pytest.raises(IssueDoesNotExist):
        get_issue(bound_issue1.object_id)


def test_delete_issue_with_timesheets(
        post_timesheet,
        authorized_api_request,
        post_issue,
        put_project,
        get_timesheets
):
    project = create_project()
    put_project(project)
    bound_issue = post_issue(project.project_id, create_issue())
    post_timesheet(bound_issue.object_id, create_timesheet())
    request = authorized_api_request("DELETE", get_issue_url(str(bound_issue.object_id)))
    assert request.status_code == 200
    assert not get_timesheets(bound_issue.object_id)


def test_delete_issue_with_expenditures(
        post_expenditure,
        authorized_api_request,
        post_issue,
        put_project,
        get_expenditures
):
    project = create_project()
    put_project(project)
    bound_issue = post_issue(project.project_id, create_issue())
    post_expenditure(bound_issue.object_id, create_expenditure())
    request = authorized_api_request("DELETE", get_issue_url(str(bound_issue.object_id)))
    assert request.status_code == 200
    assert not get_expenditures(bound_issue.object_id)


def test_create_issue_for_non_existing_project(authorized_api_request):
    response = authorized_api_request(
        "POST",
        get_project_issues_url("PRJ"),
        {"issue": MINIMAL_SERIALIZED_ISSUE}
    )
    assert response.status_code == 404
