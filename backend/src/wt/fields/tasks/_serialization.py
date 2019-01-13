from typing import List
from wt.fields.tasks._obj import Task


class TaskSerializer:
    @staticmethod
    def serialize_task(task: Task) -> dict:
        return {
            "task": task.task,
            "completed": task.completed,
        }

    def serialize_tasks(self, tasks: List[Task]):
        return [
            self.serialize_task(task)
            for task in tasks
        ]


class TaskDeserializer:
    @staticmethod
    def deserialize_task(task: dict) -> Task:
        return Task(
            task=task["task"],
            completed=task["completed"],
        )

    def deserialize_tasks(self, tasks):
        return [
            self.deserialize_task(task)
            for task
            in tasks
        ]
