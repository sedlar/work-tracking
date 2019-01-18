import transaction
from flask_injector import inject

from wt.http_api._common import handle_errors, DUMMY_STATS
from wt.entities.projects import ProjectsApi, ProjectsDeserializer, ProjectsSerializer
from wt.entities.deliverables import DeliverableSerializer, DeliverableDeserializer, DeliverablesApi
from wt.entities.issues import IssuesDeserializer, IssuesSerializer, IssuesApi
from wt.ids import EntityId


@inject
@handle_errors
def get_project(projects_api: ProjectsApi, serializer: ProjectsSerializer, project_id):
    with transaction.manager:
        project = projects_api.get_project(EntityId(project_id))
    serialized_project = serializer.serialize_project(project)
    return {
        "project": serialized_project,
        "stats": DUMMY_STATS,
    }, 200


@inject
@handle_errors
def get_projects(projects_api: ProjectsApi, serializer: ProjectsSerializer, offset, limit):
    # pylint: disable=unused-argument
    with transaction.manager:
        projects = projects_api.get_projects(offset, limit)
    serialized_projects = serializer.serialize_projects(projects)
    return {"projects": serialized_projects}, 200


@inject
@handle_errors
def put_project(projects_api: ProjectsApi, deserializer: ProjectsDeserializer, project_id, body):
    project = deserializer.deserialize_project(project_id, body["project"])
    with transaction.manager:
        projects_api.put_project(project)
    return {}, 201


@inject
@handle_errors
def delete_project(projects_api: ProjectsApi, project_id):
    with transaction.manager:
        projects_api.delete_project(EntityId(project_id))
    return {}, 200


@inject
@handle_errors
def get_project_deliverables(
        deliverables_api: DeliverablesApi,
        serializer: DeliverableSerializer,
        project_id,
        offset,
        limit,
        related_object_id=None,
):
    # pylint: disable=too-many-arguments
    with transaction.manager:
        deliverables = deliverables_api.get_deliverables(
            EntityId(project_id),
            related_entity_id=EntityId(related_object_id) if related_object_id else None,
            offset=offset,
            limit=limit
        )
    return {"deliverables": serializer.serialize_deliverables(deliverables)}, 200


@inject
@handle_errors
def post_deliverable(
        deliverables_api: DeliverablesApi,
        deserializer: DeliverableDeserializer,
        project_id,
        body,
):
    deliverable = deserializer.deserialize_deliverable(body["deliverable"])
    with transaction.manager:
        bound_deliverable = deliverables_api.create_deliverable(EntityId(project_id), deliverable)
    return {"id": bound_deliverable.object_id.full_id}, 201


def get_project_issues(
        issues_api: IssuesApi,
        serializer: IssuesSerializer,
        project_id,
        offset,
        limit,
        related_object_id=None,
):
    # pylint: disable=too-many-arguments
    with transaction.manager:
        issues = issues_api.get_issues(
            EntityId(project_id),
            related_entity_id=EntityId(related_object_id) if related_object_id else None,
            offset=offset,
            limit=limit,
        )
    return {"issues": serializer.serialize_issues(issues)}, 200


def post_issue(
        issues_api: IssuesApi,
        deserializer: IssuesDeserializer,
        project_id,
        body,
):
    issue = deserializer.deserialize_issue(body["issue"])
    with transaction.manager:
        bound_issue = issues_api.create_issue(EntityId(project_id), issue)
    return {"id": bound_issue.object_id.full_id}, 201
