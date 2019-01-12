from typing import List

from wt.fields.tasks._obj import Task


class TasksModel:
    def set_object_tasks(self, object_id: str, tasks: List[Task]):
        raise NotImplementedError()

    def get_object_tasks(self, object_id: str) -> List[Task]:
        raise NotImplementedError()
