from tests.integration.factories.objs import create_project, create_deliverable
from tests.integration.http.test_projects import get_project_url


def test_project_with_children_cant_be_deleted(
        authorized_api_request,
        post_deliverable,
        put_project
):
    project = create_project()
    put_project(project)
    post_deliverable(project.project_id, create_deliverable())

    response = authorized_api_request("DELETE", get_project_url(project.project_id))
    assert response.status_code == 400
    assert response.json["code"] == "project_has_child_elements"
