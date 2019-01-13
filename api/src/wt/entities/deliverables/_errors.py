from wt.common.errors import ObjectDoesNotExist, ErrorCodes
from wt.ids import EntityId


class DeliverableDoesNotExist(ObjectDoesNotExist):
    error_code = ErrorCodes.deliverable_does_not_exist

    def __init__(self, object_id: EntityId):
        super().__init__("Deliverable", object_id)
