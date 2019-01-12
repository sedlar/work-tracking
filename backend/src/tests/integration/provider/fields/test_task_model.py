import pytest

from tests.integration.factories.objs import create_task
from wt.fields.tasks import DuplicateTaskReceived

OBJECT_ID = "PRJ-15"


def test_add_tasks(tasks_model):
    tasks = [create_task("a"), create_task("b")]
    tasks_model.set_object_tasks(OBJECT_ID, tasks)
    saved_tasks = tasks_model.get_object_tasks(OBJECT_ID)
    assert tasks == saved_tasks


def test_add_more_tasks(tasks_model):
    original_tasks = [create_task("a"), create_task("b")]
    tasks_model.set_object_tasks(OBJECT_ID, original_tasks)

    tasks = [create_task("a"), create_task("b"), create_task("c")]
    tasks_model.set_object_tasks(OBJECT_ID, tasks)

    saved_tasks = tasks_model.get_object_tasks(OBJECT_ID)
    assert tasks == saved_tasks


def test_remove_tasks(tasks_model):
    original_tasks = [create_task("a"), create_task("b")]
    tasks_model.set_object_tasks(OBJECT_ID, original_tasks)

    tasks = [create_task("a")]
    tasks_model.set_object_tasks(OBJECT_ID, tasks)

    saved_tasks = tasks_model.get_object_tasks(OBJECT_ID)
    assert tasks == saved_tasks


def test_add_remove_tasks(tasks_model):
    original_tasks = [create_task("a"), create_task("b")]
    tasks_model.set_object_tasks(OBJECT_ID, original_tasks)

    tasks = [create_task("b"), create_task("c")]
    tasks_model.set_object_tasks(OBJECT_ID, tasks)

    saved_tasks = tasks_model.get_object_tasks(OBJECT_ID)
    assert tasks == saved_tasks


def test_duplicate_tasks(tasks_model):
    tasks = [create_task("a"), create_task("a")]
    with pytest.raises(DuplicateTaskReceived):
        tasks_model.set_object_tasks(OBJECT_ID, tasks)
