import pytest

from tests.integration.factories.objs import create_project, create_issue, create_money
from tests.integration.http.conftest import EMPTY_STATS
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


def get_project_issues_url(project_id: str):
    return "{base_project}/{project_id}{base}".format(
        project_id=project_id,
        base=BASE_ISSUES_URL,
        base_project=BASE_PROJECTS_URL,
    )


def get_issue_url(issue_id: str):
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
    "issue,serialized_issue",
    [
        [FULL_ISSUE, FULL_SERIALIZED_ISSUE,],
        [MINIMAL_ISSUE, MINIMAL_SERIALIZED_ISSUE,],
    ]
)
def test_get_issue(
        authorized_api_request,
        post_issue,
        issue,
        serialized_issue,
        put_project
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
        "stats": EMPTY_STATS,
    }


def test_get_issues(authorized_api_request, post_issue, put_project):
    project = create_project()
    put_project(project)
    minimal_bound_issue = post_issue(project.project_id, MINIMAL_ISSUE)
    full_bound_issue = post_issue(project.project_id, FULL_ISSUE)

    response = authorized_api_request("GET", get_project_issues_url(project.project_id))

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


def test_get_issues_limit(authorized_api_request, post_issue, put_project):
    project = create_project()
    put_project(project)
    minimal_bound_issue = post_issue(project.project_id, MINIMAL_ISSUE)
    post_issue(project.project_id, FULL_ISSUE)

    response = authorized_api_request(
        "GET",
        get_project_issues_url(project.project_id) + "?limit=1"
    )

    assert response.status_code == 200
    assert response.json["issues"][0]["id"] == str(minimal_bound_issue.object_id)
    del response.json["issues"][0]["id"]
    assert response.json == {"issues": [MINIMAL_SERIALIZED_ISSUE]}


def test_get_issues_offset(authorized_api_request, post_issue, put_project):
    project = create_project()
    put_project(project)
    post_issue(project.project_id, MINIMAL_ISSUE)
    full_bound_issue = post_issue(project.project_id, FULL_ISSUE)

    response = authorized_api_request(
        "GET",
        get_project_issues_url(project.project_id) + "?offset=1"
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
