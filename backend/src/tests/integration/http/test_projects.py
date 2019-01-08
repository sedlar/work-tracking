import pytest

from tests.integration.factories.objs import create_project
from wt.projects import ProjectDoesNotExist

BASE_PROJECTS_URL = "/projects"


EMPTY_STATS = {
    "progress": 0,
    "bilance_cost": {
        "amount": 0,
        "currency": "CZK"
    },
    "bilance_duration": 0,
}
MINIMAL_SERIALIZED_PROJECT = {
        "date_opened": "2019-01-01T10:30:05",
        "description": "Description",
        "files": [],
        "goals_and_metrics": "Goals and Metrics",
        "hour_rate": {
            "amount": 600.5,
            "currency": "CZK"
        },
        "limitations_and_restrictions": "Limitations and Restrictions",
        "name": "Dummy project",
        "primary_color": "#343434",
        "secondary_color": "#a1a1a1",
        "status": "open"
}
FULL_SERIALIZED_PROJECT = {
        "date_opened": "2019-01-01T10:30:05",
        "date_closed": "2019-01-02T10:30:05",
        "deadline": "2019-01-03T10:30:05",
        "description": "Description",
        "files": [
            "File1", "File2"
        ],
        "goals_and_metrics": "Goals and Metrics",
        "hour_rate": {
            "amount": 600.5,
            "currency": "CZK"
        },
        "limitations_and_restrictions": "Limitations and Restrictions",
        "name": "Dummy project",
        "primary_color": "#343434",
        "secondary_color": "#a1a1a1",
        "status": "open"
}

MINIMAL_PROJECT = create_project(project_id="ABC", date_closed=None, deadline=None, files=[])
FULL_PROJECT = create_project()


def get_project_url(project_id:str):
    return "{base}/{project_id}".format(project_id=project_id, base=BASE_PROJECTS_URL)


@pytest.mark.parametrize(
    "serialized_project,project",
    [
        [
            FULL_SERIALIZED_PROJECT, FULL_PROJECT,
        ],
        [
            MINIMAL_SERIALIZED_PROJECT, MINIMAL_PROJECT,
        ],
    ]
)
def test_put_project(authorized_api_request, get_project, serialized_project, project):
    response = authorized_api_request(
        "PUT",
        get_project_url(project.project_id),
        {"project": serialized_project}
    )
    assert response.status_code == 201

    project = get_project(project.project_id)
    assert project.__dict__ == project.__dict__


def test_put_existing_project(authorized_api_request, get_project):
    authorized_api_request(
        "PUT",
        get_project_url(FULL_PROJECT.project_id),
        {"project": MINIMAL_SERIALIZED_PROJECT}
    )
    response = authorized_api_request(
        "PUT",
        get_project_url(FULL_PROJECT.project_id),
        {"project": FULL_SERIALIZED_PROJECT}
    )
    assert response.status_code == 201

    project = get_project(FULL_PROJECT.project_id)
    assert project.__dict__ == project.__dict__


def test_get_missing_project(authorized_api_request):
    response = authorized_api_request("GET", get_project_url("AAA"))
    assert response.status_code == 404


@pytest.mark.parametrize(
    "project,serialized_project",
    [
        [FULL_PROJECT, FULL_SERIALIZED_PROJECT,],
        [MINIMAL_PROJECT, MINIMAL_SERIALIZED_PROJECT,],
    ]
)
def test_get_project(authorized_api_request, put_project, project, serialized_project):
    put_project(project)

    response = authorized_api_request("GET", get_project_url(project.project_id))

    assert response.status_code == 200
    assert response.json["project"]["id"] == project.project_id
    del response.json["project"]["id"]
    assert response.json == {
        "project": serialized_project,
        "stats": EMPTY_STATS,
    }


def test_get_projects(authorized_api_request, put_project):
    put_project(FULL_PROJECT)
    put_project(MINIMAL_PROJECT)

    response = authorized_api_request("GET", BASE_PROJECTS_URL)

    assert response.status_code == 200
    assert response.json["projects"][0]["id"] == MINIMAL_PROJECT.project_id
    assert response.json["projects"][1]["id"] == FULL_PROJECT.project_id
    del response.json["projects"][0]["id"]
    del response.json["projects"][1]["id"]
    assert response.json == {"projects": [MINIMAL_SERIALIZED_PROJECT, FULL_SERIALIZED_PROJECT]}


def test_get_projects_limit(authorized_api_request, put_project):
    put_project(FULL_PROJECT)
    put_project(MINIMAL_PROJECT)

    response = authorized_api_request("GET", BASE_PROJECTS_URL + "?limit=1")

    assert response.status_code == 200
    assert response.json["projects"][0]["id"] == MINIMAL_PROJECT.project_id
    del response.json["projects"][0]["id"]
    assert response.json == {"projects": [MINIMAL_SERIALIZED_PROJECT]}


def test_get_projects_offset(authorized_api_request, put_project):
    put_project(FULL_PROJECT)
    put_project(MINIMAL_PROJECT)

    response = authorized_api_request("GET", BASE_PROJECTS_URL + "?offset=1")

    assert response.status_code == 200
    assert response.json["projects"][0]["id"] == FULL_PROJECT.project_id
    del response.json["projects"][0]["id"]
    assert response.json == {"projects": [FULL_SERIALIZED_PROJECT]}


def test_delete_project(authorized_api_request, put_project, get_project):
    project = create_project()
    put_project(project)

    authorized_api_request("DELETE", get_project_url(project.project_id))

    with pytest.raises(ProjectDoesNotExist):
        get_project(project.project_id)
