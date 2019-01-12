from wt.common.errors import ObjectDoesNotExist, ErrorCodes, BadRequest
from wt.entities.ids import EntityId


class ProjectDoesNotExist(ObjectDoesNotExist):
    error_code = ErrorCodes.project_does_not_exist

    def __init__(self, project_id: EntityId):
        super().__init__("Project", project_id)


class ProjectHasChildElements(BadRequest):
    error_code = ErrorCodes.project_has_child_elements

    def __init__(self, object_types):
        super().__init__()
        self.message = "Project has child elements [{types}]".format(
            types=", ".join([object_type.value for object_type in object_types])
        )
