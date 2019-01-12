from typing import List

from wt.fields.tags._obj import Tag


class TagsModel:
    def set_object_tags(self, object_id: str, tags: List[Tag]):
        raise NotImplementedError()

    def get_object_tags(self, object_id: str) -> List[Tag]:
        raise NotImplementedError()
