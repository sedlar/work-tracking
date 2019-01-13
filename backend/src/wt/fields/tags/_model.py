from typing import List

from wt.ids import EntityId
from wt.fields.tags._obj import Tag


class TagsModel:
    def set_entity_tags(self, entity_id: EntityId, tags: List[Tag]):
        raise NotImplementedError()

    def get_entity_tags(self, entity_id: EntityId) -> List[Tag]:
        raise NotImplementedError()
