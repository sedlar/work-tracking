from wt.fields._base_objs import FieldItem


class Task(FieldItem):
    def __init__(self, task: str, completed: bool):
        self.task = task
        self.completed = completed

    def __eq__(self, other):
        if isinstance(other, Task):
            return self.task == other.task
        return NotImplemented
