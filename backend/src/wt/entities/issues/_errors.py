from wt.entities.ids import EntityId
from wt.common.errors import ObjectDoesNotExist, ErrorCodes


class IssueDoesNotExist(ObjectDoesNotExist):
    error_code = ErrorCodes.issue_does_not_exist

    def __init__(self, object_id: EntityId):
        super().__init__("Issue", object_id)
