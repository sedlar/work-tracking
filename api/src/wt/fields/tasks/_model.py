from typing import List

from wt.ids import BaseId
from wt.fields.tasks._obj import Task


class TasksModel:
    def set_entity_tasks(self, entity_id: BaseId, tasks: List[Task]):
        raise NotImplementedError()

    def get_entity_tasks(self, entity_id: BaseId) -> List[Task]:
        raise NotImplementedError()
