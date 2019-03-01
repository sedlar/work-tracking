from pytest import mark
from wt.ids import EntityId
from tests.integration.http.test_projects import BASE_PROJECTS_URL, get_project_url
from tests.integration.http.test_deliverables import (
    BASE_DELIVERABLES_URL,
    get_project_deliverables_url,
    get_deliverable_url,
)
from tests.integration.http.test_issues import (
    BASE_ISSUES_URL,
    get_project_issues_url,
    get_issue_url,
)
from tests.integration.http.test_expenditures import BASE_EXPENDITURE_URL, get_expenditure_url
from tests.integration.http.test_timesheets import BASE_TIMESHEET_URL, get_timesheet_url
from tests.integration.http.test_links import get_link_url

ID1 = EntityId("AAA-1")
ID2 = EntityId("AAA-2")

@mark.parametrize(
    "method,url",
    [
        ["GET", get_project_url("AAA")],
        ["PUT", get_project_url("AAA")],
        ["DELETE", get_project_url("AAA")],
        ["GET", BASE_PROJECTS_URL],

        ["PUT", get_link_url(ID1, ID2)],
        ["DELETE", get_link_url(ID1, ID2)],

        ["GET", BASE_DELIVERABLES_URL],
        ["GET", get_deliverable_url(ID1)],
        ["PUT", BASE_DELIVERABLES_URL],
        ["DELETE", get_deliverable_url(ID1)],
        ["PUT", get_project_deliverables_url("PRJ")],
        ["DELETE", get_project_deliverables_url("PRJ")],

        ["GET", BASE_ISSUES_URL],
        ["GET", get_issue_url(ID1)],
        ["PUT", BASE_ISSUES_URL],
        ["DELETE", get_issue_url(ID1)],
        ["PUT", get_project_issues_url("PRJ")],
        ["DELETE", get_project_issues_url("PRJ")],

        ["GET", get_expenditure_url(ID1)],
        ["POST", get_expenditure_url(ID1)],
        ["DELETE", get_expenditure_url(1)],

        ["GET", get_timesheet_url(ID1)],
        ["POST", get_timesheet_url(ID1)],
        ["DELETE", get_timesheet_url(1)],
    ]
)
def test_authorization(api_request, method, url):
    response = api_request("GET", get_project_url("AAA"))
    assert response.status_code == 401