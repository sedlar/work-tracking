from pytest import mark
from tests.integration.http.test_projects import BASE_PROJECTS_URL, get_project_url


@mark.parametrize(
    "method,url",
    [
        ["GET", get_project_url("AAA")],
        ["PUT", get_project_url("AAA")],
        ["DELETE", get_project_url("AAA")],
        ["GET", BASE_PROJECTS_URL],

    ]
)
def test_authorization(api_request, method, url):
    response = api_request("GET", get_project_url("AAA"))
    assert response.status_code == 401