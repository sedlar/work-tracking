from typing import List

from wt.ids import EntityId
from wt.fields.links._obj import Link


class LinksModel:
    def set_entity_links(self, entity_id: EntityId, links: List[Link]):
        raise NotImplementedError()

    def get_entity_links(self, entity_id: EntityId) -> List[Link]:
        raise NotImplementedError()
