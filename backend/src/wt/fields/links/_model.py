from typing import List

from wt.fields.links._obj import Link


class LinksModel:
    def set_object_links(self, object_id: str, links: List[Link]):
        raise NotImplementedError()

    def get_object_links(self, object_id: str) -> List[Link]:
        raise NotImplementedError()
