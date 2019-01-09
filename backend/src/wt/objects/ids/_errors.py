from typing import List
from wt.objects.ids._obj import ObjectId


class ObjectsDoesNotExist(Exception):
    def __init__(self, object_ids: List[ObjectId]):
        super().__init__()
        self.message = "Objects [{object_ids}] doesn't exist.".format(
            object_ids=[object_id.object_id for object_id in object_ids]
        )
