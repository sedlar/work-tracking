from enum import Enum
from functools import wraps

import transaction
from flask_injector import inject

from wt.projects import ProjectsApi, ProjectDeserializer, ProjectSerializer, ProjectDoesNotExist


class ErrorCodes(Enum):
    project_does_not_exist = "project_does_not_exist"


def get_error_response(error_code, message):
    return {
        "code": error_code.value,
        "message": message
    }


def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ProjectDoesNotExist as ex:
            return get_error_response(
                ErrorCodes.project_does_not_exist,
                ex.message
            ), 404

    return wrapper


PROJECT_STATS = {
    "progress": 0,
    "bilance_duration": 0,
    "bilance_cost": {
        "amount": 0,
        "currency": "CZK",
    },
}


@inject
@handle_errors
def get_project(projects_api: ProjectsApi, serializer: ProjectSerializer, project_id):
    with transaction.manager:
        project = projects_api.get_project(project_id)
    serialized_project = serializer.serialize_project(project)
    return {
        "project": serialized_project,
        "stats": PROJECT_STATS,
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
        projects_api.delete_project(project_id)
    return {}, 200


def get_project_deliverables():
    return "NOT IMPLEMENTED", 500


def get_project_issues():
    return "NOT IMPLEMENTED", 500


def post_deliverable():
    return "NOT IMPLEMENTED", 500


def post_issue():
    return "NOT IMPLEMENTED", 500
