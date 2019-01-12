from typing import List

from wt.common.errors import DuplicateObjectReceived


class DuplicateTaskReceived(DuplicateObjectReceived):
    def __init__(self, duplicate_tasks: List[str]):
        super().__init__()
        self.message = "Object tasks need to be unique [{duplicate_tasks}].".format(
            duplicate_tasks=duplicate_tasks
        )
