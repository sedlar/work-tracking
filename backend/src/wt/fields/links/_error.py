from typing import List

from wt.common.errors import DuplicateObjectReceived


class DuplicateLinkSent(DuplicateObjectReceived):
    def __init__(self, duplicate_uris: List[str]):
        super().__init__()
        self.message = "Object link uris need to be unique [{duplicate_uris}].".format(
            duplicate_uris=duplicate_uris
        )
