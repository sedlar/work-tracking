from enum import Enum
from wt.ids import EntityId, EntityType


class ErrorCodes(Enum):
    project_does_not_exist = "project_does_not_exist"
    project_has_child_elements = "project_has_child_elements"
    issue_does_not_exist = "issue_does_not_exist"
    deliverable_does_not_exist = "deliverable_does_not_exist"
    link_already_exists = "link_already_exists"
    link_does_not_exist = "link_does_not_exist"
    invalid_link_to_itself = "invalid_link_to_itself"
    invalid_linked_entities = "invalid_linked_entities"
    invalid_link_between_projects = "invalid_link_between_projects"
    duplicate_object_received = "duplicate_object_received"
    invalid_parent_type = "invalid_parent_type"
    object_does_not_exist = "object_does_not_exist"


class BadRequest(Exception):
    error_code = ""
    message = ""


class ObjectDoesNotExist(BadRequest):
    error_code = ErrorCodes.object_does_not_exist

    def __init__(self, obj, entity_id: EntityId):
        super().__init__()
        self.message = "{obj} '{id}' does not exist.".format(obj=obj, id=entity_id.full_id)


class DuplicateObjectReceived(Exception):
    error_code = ErrorCodes.duplicate_object_received


class InvalidParentType(BadRequest):
    error_code = ErrorCodes.invalid_parent_type

    def __init__(self, parent_type: EntityType):
        super().__init__()
        self.message = "Parent object cant't be {type}".format(type=parent_type.value)
