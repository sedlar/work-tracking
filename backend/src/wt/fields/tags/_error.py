from typing import List

from wt.common.errors import DuplicateObjectReceived


class DuplicateTagReceived(DuplicateObjectReceived):
    def __init__(self, duplicate_tags: List[str]):
        super().__init__()
        self.message = "Object tags need to be unique [{duplicate_tags}].".format(
            duplicate_tags=duplicate_tags
        )
