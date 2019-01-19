from tests.integration.factories.objs import (
    create_expenditure,
    create_project, create_issue,
    create_deliverable,
)
from wt.costs.expenditures import BoundExpenditure
from wt.ids import EntityId

BASE_EXPENDITURE_URL = "/expenditures/"
MINIMAL_SERIALIZED_EXPENDITURE = {
    "name": "Expenditure name",
    "description": "Expenditure description",
    "status": "approved",
    "type": "freelance",
    "date_opened": "2005-04-08T00:00:00Z",
    "files": [],
    "cost": {
        "amount": 600.5,
        "currency": "CZK",
    }
}
FULL_SERIALIZED_EXPENDITURE = {
    "name": "Expenditure name",
    "description": "Expenditure description",
    "status": "approved",
    "type": "freelance",
    "date_opened": "2005-04-08T00:00:00Z",
    "date_closed": "2005-04-09T00:00:00Z",
    "deadline": "2005-04-10T00:00:00Z",
    "files": ["ExpFile1", "ExpFile2"],
    "cost": {
        "amount": 600.5,
        "currency": "CZK",
    }
}
MINIMAL_EXPENDITURE = create_expenditure(
    date_closed=None,
    deadline=None,
    files=[],
)
FULL_EXPENDITURE = create_expenditure()


def get_expenditure_url(id_):
    return BASE_EXPENDITURE_URL + str(id_)


def test_post_minimal_expenditure(
        put_project,
        post_issue,
        authorized_api_request,
        get_expenditures
):
    project = create_project()
    put_project(project)
    bound_issue = post_issue(project.project_id, create_issue())
    response = authorized_api_request(
        "POST",
        get_expenditure_url(bound_issue.object_id),
        {"expenditure": MINIMAL_SERIALIZED_EXPENDITURE}
    )
    assert response.status_code == 201
    expenditures = get_expenditures(bound_issue.object_id)
    assert len(expenditures) == 1
    assert expenditures[0] == BoundExpenditure(
        simple_id=expenditures[0].simple_id,
        expenditure=MINIMAL_EXPENDITURE,
    )


def test_post_full_expenditure(put_project, post_issue, authorized_api_request, get_expenditures):
    project = create_project()
    put_project(project)
    bound_issue = post_issue(project.project_id, create_issue())
    response = authorized_api_request(
        "POST",
        get_expenditure_url(bound_issue.object_id),
        {"expenditure": FULL_SERIALIZED_EXPENDITURE}
    )
    assert response.status_code == 201
    expenditures = get_expenditures(bound_issue.object_id)
    assert len(expenditures) == 1
    assert expenditures[0] == BoundExpenditure(
        simple_id=expenditures[0].simple_id,
        expenditure=FULL_EXPENDITURE,
    )


def test_delete_expenditure(
        post_expenditure,
        authorized_api_request,
        post_issue,
        put_project,
        get_expenditures
):
    project = create_project()
    put_project(project)
    bound_issue = post_issue(project.project_id, create_issue())
    bound_expenditure = post_expenditure(bound_issue.object_id, create_expenditure())
    response = authorized_api_request(
        "DELETE",
        get_expenditure_url(bound_expenditure.simple_id.simple_id),
    )
    assert response.status_code == 200
    assert not get_expenditures(bound_issue.object_id)


def test_get_minimal_expenditures(
        post_expenditure,
        authorized_api_request,
        post_issue,
        put_project,
):
    project = create_project()
    put_project(project)
    bound_issue = post_issue(project.project_id, create_issue())
    bound_expenditure = post_expenditure(bound_issue.object_id, MINIMAL_EXPENDITURE)
    response = authorized_api_request(
        "GET",
        get_expenditure_url(bound_issue.object_id),
        )
    assert response.status_code == 200
    assert len(response.json["expenditures"]) == 1
    assert response.json["expenditures"][0] == {
        **MINIMAL_SERIALIZED_EXPENDITURE,
        "id": bound_expenditure.simple_id.simple_id
    }


def test_get_full_expenditures(
        post_expenditure,
        authorized_api_request,
        post_issue,
        put_project,
):
    project = create_project()
    put_project(project)
    bound_issue = post_issue(project.project_id, create_issue())
    bound_expenditure = post_expenditure(bound_issue.object_id, FULL_EXPENDITURE)
    response = authorized_api_request(
        "GET",
        get_expenditure_url(bound_issue.object_id),
        )
    assert response.status_code == 200
    assert len(response.json["expenditures"]) == 1
    assert response.json["expenditures"][0] == {
        **FULL_SERIALIZED_EXPENDITURE,
        "id": bound_expenditure.simple_id.simple_id
    }


def test_get_expenditures_offset(post_expenditure, authorized_api_request, post_issue, put_project):
    project = create_project()
    put_project(project)
    bound_issue = post_issue(project.project_id, create_issue())
    post_expenditure(bound_issue.object_id, create_expenditure())
    bound_expenditure = post_expenditure(
        bound_issue.object_id,
        create_expenditure(description="offset")
    )
    response = authorized_api_request(
        "GET",
        get_expenditure_url(bound_issue.object_id) + "?offset=1",
        )
    assert response.status_code == 200
    assert len(response.json["expenditures"]) == 1
    assert response.json["expenditures"][0]["description"] == bound_expenditure.description


def test_get_expenditures_limit(post_expenditure, authorized_api_request, post_issue, put_project):
    project = create_project()
    put_project(project)
    bound_issue = post_issue(project.project_id, create_issue())
    bound_expenditure = post_expenditure(
        bound_issue.object_id,
        create_expenditure(description="limit")
    )
    post_expenditure(bound_issue.object_id, create_expenditure())
    response = authorized_api_request(
        "GET",
        get_expenditure_url(bound_issue.object_id) + "?limit=1",
        )
    assert response.status_code == 200
    assert len(response.json["expenditures"]) == 1
    assert response.json["expenditures"][0]["description"] == bound_expenditure.description


def test_create_expenditure_for_invalid_entity(
        authorized_api_request,
        post_deliverable,
        put_project
):
    project = create_project()
    put_project(project)
    bound_deliverable = post_deliverable(project.project_id, create_deliverable())
    response = authorized_api_request(
        "POST",
        get_expenditure_url(bound_deliverable.object_id),
        {"expenditure": MINIMAL_SERIALIZED_EXPENDITURE}
    )
    assert response.status_code == 400
    assert response.json["code"] == "invalid_parent_type"


def test_create_expenditure_non_existing_entity(authorized_api_request):
    response = authorized_api_request(
        "POST",
        get_expenditure_url(EntityId("ABC-1")),
        {"expenditure": MINIMAL_SERIALIZED_EXPENDITURE}
    )
    assert response.status_code == 404
    assert response.json["code"] == "object_does_not_exist"
