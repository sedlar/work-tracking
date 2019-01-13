import transaction
from flask_injector import inject

from wt.http_api._common import DUMMY_STATS
from wt.http_api._common import handle_errors
from wt.entities.issues import IssueSerializer, IssueDeserializer, IssuesApi
from wt.ids import EntityId


@inject
@handle_errors
def get_issue(
        issues_api: IssuesApi,
        serializer: IssueSerializer,
        issue_id,
):
    with transaction.manager:
        issue = issues_api.get_issue(EntityId(issue_id))

    return {
        "issue": serializer.serialize_issue(issue),
        "stats": DUMMY_STATS,
    }, 200


@inject
@handle_errors
def put_issue(
        issues_api: IssuesApi,
        deserializer: IssueDeserializer,
        issue_id,
        body,
):
    issue = deserializer.deserialize_bound_issue(
        issue_id,
        body["issue"]
    )
    with transaction.manager:
        issues_api.edit_issue(issue)
    return {}, 200


@inject
@handle_errors
def delete_issue(
        issues_api: IssuesApi,
        issue_id
):
    with transaction.manager:
        issues_api.delete_issue(EntityId(issue_id))
    return {}, 200


def get_issue_timesheets():
    return "NOT IMPLEMENTED", 500


def get_issue_expenditures():
    return "NOT IMPLEMENTED", 500


def post_issue_timesheet():
    return "NOT IMPLEMENTED", 500


def post_issue_expenditure():
    return "NOT IMPLEMENTED", 500
