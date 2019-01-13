from enum import Enum
from wt.entities.ids import EntityId


class ErrorCodes(Enum):
    project_does_not_exist = "project_does_not_exist"
    project_has_child_elements = "project_has_child_elements"
    issue_does_not_exist = "issue_does_not_exist"
    deliverable_does_not_exist = "deliverable_does_not_exist"


class BadRequest(Exception):
    error_code = ""
    message = ""


class ObjectDoesNotExist(Exception):
    error_code = ""

    def __init__(self, obj, entity_id: EntityId):
        super().__init__()
        self.message = "{obj} '{id}' does not exist.".format(obj=obj, id=entity_id.full_id)


class DuplicateObjectReceived(Exception):
    error_code = "duplicate_object_received"
