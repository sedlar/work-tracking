from typing import List

from wt.ids import BaseId
from wt.fields.tags._obj import Tag


class TagsModel:
    def set_entity_tags(self, entity_id: BaseId, tags: List[Tag]):
        raise NotImplementedError()

    def get_entity_tags(self, entity_id: BaseId) -> List[Tag]:
        raise NotImplementedError()
