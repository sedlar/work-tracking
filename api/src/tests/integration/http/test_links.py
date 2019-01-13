from tests.integration.factories.objs import create_project, create_issue
from wt.ids import EntityId

ID1 = EntityId("AAA-1")
ID2 = EntityId("AAA-2")


def get_link_url(entity_id, other_entity_id):
    return "/links/{entity_id}/{other_entity_id}".format(
        entity_id=entity_id.full_id,
        other_entity_id=other_entity_id.full_id,
    )


def test_create_link(authorized_api_request, post_issue, put_project):
    project = create_project()
    put_project(project)
    issue1 = post_issue(project.project_id, create_issue())
    issue2 = post_issue(project.project_id, create_issue())

    response = authorized_api_request(
        "PUT",
        get_link_url(issue1.object_id, issue2.object_id)
    )
    assert response.status_code == 201


def test_create_invalid_link(authorized_api_request):
    response = authorized_api_request(
        "PUT",
        get_link_url(ID1, ID1)
    )
    assert response.status_code == 400


def test_delete_link(authorized_api_request, put_project, post_issue, post_link):
    project = create_project()
    put_project(project)
    issue1 = post_issue(project.project_id, create_issue())
    issue2 = post_issue(project.project_id, create_issue())
    post_link(issue1.object_id, issue2.object_id)

    response = authorized_api_request(
        "DELETE",
        get_link_url(issue1.object_id, issue2.object_id)
    )
    assert response.status_code == 200


def test_delete_missing_link(authorized_api_request):
    response = authorized_api_request(
        "DELETE",
        get_link_url(ID1, ID2)
    )
    assert response.status_code == 400
