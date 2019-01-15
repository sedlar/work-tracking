from typing import List

from wt.ids import BaseId
from wt.fields.links._obj import Link


class LinksModel:
    def set_entity_links(self, entity_id: BaseId, links: List[Link]):
        raise NotImplementedError()

    def get_entity_links(self, entity_id: BaseId) -> List[Link]:
        raise NotImplementedError()
