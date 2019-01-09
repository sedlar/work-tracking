from wt.objects.ids import ObjectId, ObjectsDoesNotExist


class DeliverableDoesNotExist(ObjectsDoesNotExist):
    def __init__(self, object_id: ObjectId):
        super().__init__([object_id])
