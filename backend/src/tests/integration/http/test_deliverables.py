import pytest

from tests.integration.factories.objs import create_project, create_deliverable
from tests.integration.http.conftest import EMPTY_STATS
from tests.integration.http.test_projects import BASE_PROJECTS_URL
from wt.objects.deliverables import BoundDeliverable
from wt.objects.deliverables import DeliverableDoesNotExist
from wt.objects.ids import ObjectId

BASE_DELIVERABLES_URL = "/deliverables"


MINIMAL_SERIALIZED_DELIVERABLE = {
        "date_opened": "2019-01-01T10:30:05",
        "description": "Description deliverable",
        "name": "Dummy deliverable",
        "status": "open"
}
FULL_SERIALIZED_DELIVERABLE = {
        "date_opened": "2019-01-01T10:30:05",
        "date_closed": "2019-01-02T10:30:05",
        "deadline": "2019-01-03T10:30:05",
        "description": "Description deliverable",
        "name": "Dummy deliverable",
        "status": "open"
}

MINIMAL_DELIVERABLE = create_deliverable(date_closed=None, deadline=None)
FULL_DELIVERABLE = create_deliverable()


def get_project_deliverables_url(project_id: str):
    return "{base_project}/{project_id}{base}".format(
        project_id=project_id,
        base=BASE_DELIVERABLES_URL,
        base_project=BASE_PROJECTS_URL,
    )


def get_deliverable_url(deliverable_id: str):
    return "{base}/{deliverable_id}".format(
        deliverable_id=deliverable_id,
        base=BASE_DELIVERABLES_URL,
    )


@pytest.mark.parametrize(
    "serialized_deliverable,deliverable",
    [
        [
            FULL_SERIALIZED_DELIVERABLE, FULL_DELIVERABLE,
        ],
        [
            MINIMAL_SERIALIZED_DELIVERABLE, MINIMAL_DELIVERABLE,
        ],
    ]
)
def test_post_deliverable(
        authorized_api_request,
        get_deliverable,
        serialized_deliverable,
        deliverable,
        put_project,
):
    put_project(create_project())

    response = authorized_api_request(
        "POST",
        get_project_deliverables_url("PRJ"),
        {"deliverable": serialized_deliverable}
    )
    assert response.status_code == 201

    loaded_deliverable = get_deliverable(ObjectId(response.json["id"]))
    assert loaded_deliverable.__dict__ == BoundDeliverable(
        ObjectId("PRJ-1"),
        deliverable
    ).__dict__


def test_post_existing_deliverable(authorized_api_request, get_deliverable, put_project):
    put_project(create_project())

    authorized_api_request(
        "POST",
        get_project_deliverables_url("PRJ"),
        {"deliverable": MINIMAL_SERIALIZED_DELIVERABLE}
    )
    response = authorized_api_request(
        "POST",
        get_project_deliverables_url("PRJ"),
        {"deliverable": FULL_SERIALIZED_DELIVERABLE}
    )
    assert response.status_code == 201

    loaded_deliverable = get_deliverable(ObjectId(response.json["id"]))
    assert loaded_deliverable.__dict__ == BoundDeliverable(
        ObjectId("PRJ-2"),
        FULL_DELIVERABLE
    ).__dict__


def test_put_deliverable(authorized_api_request, get_deliverable, put_project):
    put_project(create_project())

    response = authorized_api_request(
        "POST",
        get_project_deliverables_url("PRJ"),
        {"deliverable": MINIMAL_SERIALIZED_DELIVERABLE}
    )
    deliverable_id = ObjectId(response.json["id"])
    response = authorized_api_request(
        "PUT",
        get_deliverable_url(deliverable_id.object_id),
        {"deliverable": FULL_SERIALIZED_DELIVERABLE}
    )
    assert response.status_code == 200

    loaded_deliverable = get_deliverable(deliverable_id)
    assert loaded_deliverable.__dict__ == BoundDeliverable(
        deliverable_id,
        FULL_DELIVERABLE
    ).__dict__


def test_put_missing_deliverable(authorized_api_request):
    response = authorized_api_request(
        "PUT",
        get_deliverable_url("AAA-3"),
        {"deliverable": FULL_SERIALIZED_DELIVERABLE}
    )
    assert response.status_code == 404


def test_get_missing_deliverable(authorized_api_request):
    response = authorized_api_request("GET", get_deliverable_url("AAA-3"))
    assert response.status_code == 404


@pytest.mark.parametrize(
    "deliverable,serialized_deliverable",
    [
        [FULL_DELIVERABLE, FULL_SERIALIZED_DELIVERABLE,],
        [MINIMAL_DELIVERABLE, MINIMAL_SERIALIZED_DELIVERABLE,],
    ]
)
def test_get_deliverable(
        authorized_api_request,
        post_deliverable,
        deliverable,
        serialized_deliverable,
        put_project
):
    project = create_project()
    put_project(project)
    bound_deliverable = post_deliverable(project.project_id, deliverable)

    response = authorized_api_request(
        "GET",
        get_deliverable_url(str(bound_deliverable.object_id))
    )

    assert response.status_code == 200
    assert response.json["deliverable"]["id"] == str(bound_deliverable.object_id)
    del response.json["deliverable"]["id"]
    assert response.json == {
        "deliverable": serialized_deliverable,
        "stats": EMPTY_STATS,
    }


def test_get_deliverables(authorized_api_request, post_deliverable, put_project):
    project = create_project()
    put_project(project)
    minimal_bound_deliverable = post_deliverable(project.project_id, MINIMAL_DELIVERABLE)
    full_bound_deliverable = post_deliverable(project.project_id, FULL_DELIVERABLE)

    response = authorized_api_request("GET", get_project_deliverables_url(project.project_id))

    assert response.status_code == 200
    assert response.json["deliverables"][0]["id"] == str(minimal_bound_deliverable.object_id)
    assert response.json["deliverables"][1]["id"] == str(full_bound_deliverable.object_id)
    del response.json["deliverables"][0]["id"]
    del response.json["deliverables"][1]["id"]
    assert response.json == {
        "deliverables":
        [
            MINIMAL_SERIALIZED_DELIVERABLE,
            FULL_SERIALIZED_DELIVERABLE
        ]
    }


def test_get_deliverables_limit(authorized_api_request, post_deliverable, put_project):
    project = create_project()
    put_project(project)
    minimal_bound_deliverable = post_deliverable(project.project_id, MINIMAL_DELIVERABLE)
    post_deliverable(project.project_id, FULL_DELIVERABLE)

    response = authorized_api_request(
        "GET",
        get_project_deliverables_url(project.project_id) + "?limit=1"
    )

    assert response.status_code == 200
    assert response.json["deliverables"][0]["id"] == str(minimal_bound_deliverable.object_id)
    del response.json["deliverables"][0]["id"]
    assert response.json == {"deliverables": [MINIMAL_SERIALIZED_DELIVERABLE]}


def test_get_deliverables_offset(authorized_api_request, post_deliverable, put_project):
    project = create_project()
    put_project(project)
    post_deliverable(project.project_id, MINIMAL_DELIVERABLE)
    full_bound_deliverable = post_deliverable(project.project_id, FULL_DELIVERABLE)

    response = authorized_api_request(
        "GET",
        get_project_deliverables_url(project.project_id) + "?offset=1"
    )

    assert response.status_code == 200
    assert response.json["deliverables"][0]["id"] == str(full_bound_deliverable.object_id)
    del response.json["deliverables"][0]["id"]
    assert response.json == {"deliverables": [FULL_SERIALIZED_DELIVERABLE]}


def test_delete_deliverable(authorized_api_request, post_deliverable, get_deliverable, put_project):
    project = create_project()
    put_project(project)
    deliverable = create_deliverable()
    bound_deliverable = post_deliverable(project.project_id, deliverable)

    authorized_api_request("DELETE", get_deliverable_url(str(bound_deliverable.object_id)))

    with pytest.raises(DeliverableDoesNotExist):
        get_deliverable(bound_deliverable.object_id)