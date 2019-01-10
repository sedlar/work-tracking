from wt.objects.ids import ObjectId
from wt.common.errors import ObjectDoesNotExist, ErrorCodes


class DeliverableDoesNotExist(ObjectDoesNotExist):
    error_code = ErrorCodes.deliverable_does_not_exist

    def __init__(self, object_id: ObjectId):
        super().__init__("Deliverable", object_id.object_id)
