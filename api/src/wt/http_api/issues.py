import transaction
from flask_injector import inject

from wt.http_api._common import DUMMY_STATS
from wt.http_api._common import handle_errors
from wt.entities.issues import IssuesSerializer, IssuesDeserializer, IssuesApi
from wt.ids import EntityId


@inject
@handle_errors
def get_issue(
        issues_api: IssuesApi,
        serializer: IssuesSerializer,
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
        deserializer: IssuesDeserializer,
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
