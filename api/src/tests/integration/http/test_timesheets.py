from tests.integration.factories.objs import (
    create_timesheet,
    create_project, create_issue,
    create_deliverable,
)
from wt.costs.timesheets import BoundTimesheet
from wt.ids import EntityId

BASE_TIMESHEET_URL = "/timesheets"
TIMESHEET = {
    "date_opened": "2002-03-13T00:00:00Z",
    "description": "Timesheet description",
    "duration": 15.5,
}


def create_timesheet_body(parent_id):
    return {
        **TIMESHEET,
        "parent_id": parent_id.full_id
    }


def get_timesheet_url(simple_id):
    return BASE_TIMESHEET_URL + "/" + str(simple_id)


def test_post_timesheet(put_project, post_issue, authorized_api_request, get_timesheets):
    project = create_project()
    put_project(project)
    bound_issue = post_issue(project.project_id, create_issue())
    response = authorized_api_request(
        "POST",
        BASE_TIMESHEET_URL,
        {"timesheet": create_timesheet_body(bound_issue.object_id)}
    )
    assert response.status_code == 201
    timesheets = get_timesheets(bound_issue.object_id)
    assert len(timesheets) == 1
    assert timesheets[0] == BoundTimesheet(
        simple_id=timesheets[0].simple_id,
        timesheet=create_timesheet(),
    )


def test_delete_timesheet(
        post_timesheet,
        authorized_api_request,
        post_issue,
        put_project,
        get_timesheets
):
    project = create_project()
    put_project(project)
    bound_issue = post_issue(project.project_id, create_issue())
    bound_timesheet = post_timesheet(bound_issue.object_id, create_timesheet())
    response = authorized_api_request(
        "DELETE",
        get_timesheet_url(bound_timesheet.simple_id.simple_id),
    )
    assert response.status_code == 200
    assert not get_timesheets(bound_issue.object_id)


def test_get_timesheets(
        post_timesheet,
        authorized_api_request,
        post_issue,
        put_project,
):
    project = create_project()
    put_project(project)
    bound_issue = post_issue(project.project_id, create_issue())
    bound_timesheet = post_timesheet(bound_issue.object_id, create_timesheet())
    response = authorized_api_request(
        "GET",
        BASE_TIMESHEET_URL + "?object_id=" + str(bound_issue.object_id),
    )
    assert response.status_code == 200
    assert len(response.json["timesheets"]) == 1
    assert response.json["timesheets"][0] == {
        **TIMESHEET,
        "id": bound_timesheet.simple_id.simple_id
    }


def test_get_timesheets_offset(post_timesheet, authorized_api_request, post_issue, put_project):
    project = create_project()
    put_project(project)
    bound_issue = post_issue(project.project_id, create_issue())
    post_timesheet(bound_issue.object_id, create_timesheet())
    bound_timesheet = post_timesheet(bound_issue.object_id, create_timesheet(description="offset"))
    response = authorized_api_request(
        "GET",
        BASE_TIMESHEET_URL + "?object_id=" + str(bound_issue.object_id) + "&offset=1",
    )
    assert response.status_code == 200
    assert len(response.json["timesheets"]) == 1
    assert response.json["timesheets"][0]["description"] == bound_timesheet.description


def test_get_timesheets_limit(post_timesheet, authorized_api_request, post_issue, put_project):
    project = create_project()
    put_project(project)
    bound_issue = post_issue(project.project_id, create_issue())
    bound_timesheet = post_timesheet(bound_issue.object_id, create_timesheet(description="limit"))
    post_timesheet(bound_issue.object_id, create_timesheet())
    response = authorized_api_request(
        "GET",
        BASE_TIMESHEET_URL + "?object_id=" + str(bound_issue.object_id) + "&limit=1",
    )
    assert response.status_code == 200
    assert len(response.json["timesheets"]) == 1
    assert response.json["timesheets"][0]["description"] == bound_timesheet.description


def test_create_timesheet_for_invalid_entity(authorized_api_request, post_deliverable, put_project):
    project = create_project()
    put_project(project)
    bound_deliverable = post_deliverable(project.project_id, create_deliverable())
    response = authorized_api_request(
        "POST",
        BASE_TIMESHEET_URL,
        {"timesheet": create_timesheet_body(bound_deliverable.object_id)}
    )
    assert response.status_code == 400
    assert response.json["code"] == "invalid_parent_type"


def test_create_timesheet_non_existing_entity(authorized_api_request):
    response = authorized_api_request(
        "POST",
        BASE_TIMESHEET_URL,
        {"timesheet": create_timesheet_body(EntityId("ABC-1"))}
    )
    assert response.status_code == 404
    assert response.json["code"] == "object_does_not_exist"
