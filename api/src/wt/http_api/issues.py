import transaction
from flask_injector import inject

from wt.entities.issues import IssuesSerializer, IssuesDeserializer, IssuesApi
from wt.http_api._common import handle_errors
from wt.ids import EntityId
from wt.statistics import StatisticsSerializer, StatisticsApi


@inject
@handle_errors
def get_issues(
        issues_api: IssuesApi,
        serializer: IssuesSerializer,
        offset,
        limit,
):
    # pylint: disable=too-many-arguments
    with transaction.manager:
        issues = issues_api.get_issues(
            project_id=None,
            related_entity_id=None,
            offset=offset,
            limit=limit,
        )
    return {"issues": serializer.serialize_issues(issues)}, 200


@inject
@handle_errors
def get_issue(
        issues_api: IssuesApi,
        statistics_api: StatisticsApi,
        serializer: IssuesSerializer,
        statistics_serializer: StatisticsSerializer,
        issue_id,
):
    issue_id = EntityId(issue_id)
    with transaction.manager:
        issue = issues_api.get_issue(issue_id)
        statistics = statistics_api.get_entity_statistics(issue_id)

    return {
        "issue": serializer.serialize_issue(issue),
        "stats": statistics_serializer.serialize_statistics(statistics),
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
