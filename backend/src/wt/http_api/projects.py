import transaction
from flask_injector import inject

from wt.http_api._common import handle_errors, DUMMY_STATS
from wt.entities.projects import ProjectsApi, ProjectDeserializer, ProjectSerializer
from wt.entities.deliverables import DeliverableSerializer, DeliverableDeserializer, DeliverablesApi
from wt.ids import EntityId


@inject
@handle_errors
def get_project(projects_api: ProjectsApi, serializer: ProjectSerializer, project_id):
    with transaction.manager:
        project = projects_api.get_project(EntityId(project_id))
    serialized_project = serializer.serialize_project(project)
    return {
        "project": serialized_project,
        "stats": DUMMY_STATS,
    }, 200


@inject
@handle_errors
def get_projects(projects_api: ProjectsApi, serializer: ProjectSerializer, offset, limit):
    # pylint: disable=unused-argument
    with transaction.manager:
        projects = projects_api.get_projects(offset, limit)
    serialized_projects = serializer.serialize_projects(projects)
    return {"projects": serialized_projects}, 200


@inject
@handle_errors
def put_project(projects_api: ProjectsApi, deserializer: ProjectDeserializer, project_id, body):
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
        limit
):
    with transaction.manager:
        deliverables = deliverables_api.get_deliverables(
            EntityId(project_id),
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


def get_project_issues():
    return "NOT IMPLEMENTED", 500


def post_issue():
    return "NOT IMPLEMENTED", 500
