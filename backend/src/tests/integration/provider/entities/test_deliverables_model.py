from datetime import datetime

import pytest

from tests.integration.factories.objs import create_bound_deliverable, create_project
from wt.entities.deliverables import DeliverableStatus, DeliverableDoesNotExist
from wt.ids import EntityId


def test_create_deliverable(deliverables_model, put_project):
    put_project(create_project())

    deliverable = create_bound_deliverable()
    deliverables_model.put_deliverable(deliverable)
    saved_deliverable = deliverables_model.get_deliverable(deliverable.object_id)
    assert deliverable == saved_deliverable


def test_update_deliverable(deliverables_model, put_project):
    put_project(create_project())

    deliverable = create_bound_deliverable()
    deliverables_model.put_deliverable(deliverable)

    updated_deliverable = create_bound_deliverable(
        name="Test",
        status=DeliverableStatus.completed,
        description="DESC",
        date_opened=datetime(year=2020, month=1, day=1, hour=10, minute=30),
        date_closed=datetime(year=2020, month=1, day=2, hour=10, minute=30),
        deadline=datetime(year=2020, month=1, day=3, hour=10, minute=30),
    )
    deliverables_model.put_deliverable(updated_deliverable)

    saved_deliverable = deliverables_model.get_deliverable(deliverable.object_id)
    assert updated_deliverable == saved_deliverable


def test_get_deliverables(deliverables_model, put_project):
    put_project(create_project())

    deliverable1 = create_bound_deliverable()
    deliverables_model.put_deliverable(deliverable1)

    deliverable2 = create_bound_deliverable(
        object_id=deliverable1.object_id.project_id + "-2",
        name="Other deliverable"
    )
    deliverables_model.put_deliverable(deliverable2)

    deliverables = deliverables_model.get_deliverables(EntityId(deliverable1.object_id.project_id), 0, 2)
    assert deliverables == [deliverable1, deliverable2]


def test_get_deliverables_filter_project(deliverables_model, put_project):
    put_project(create_project())
    put_project(create_project("AAA"))

    deliverable1 = create_bound_deliverable()
    deliverables_model.put_deliverable(deliverable1)

    deliverable2 = create_bound_deliverable(
        object_id="AAA",
        name="Other deliverable"
    )
    deliverables_model.put_deliverable(deliverable2)

    deliverables = deliverables_model.get_deliverables(
        EntityId(deliverable1.object_id.project_id),
        0,
        2
    )
    assert deliverables == [deliverable1]


def test_delete_deliverable(deliverables_model, put_project):
    put_project(create_project())

    deliverable = create_bound_deliverable()
    deliverables_model.put_deliverable(deliverable)

    deliverables_model.delete_deliverable(deliverable.object_id)
    assert not deliverables_model.get_deliverables(EntityId(deliverable.object_id.project_id), 0, 1)


def test_get_no_deliverable(deliverables_model):
    with pytest.raises(DeliverableDoesNotExist):
        deliverables_model.get_deliverable(EntityId("ABC-2"))


def test_delete_no_deliverable(deliverables_model):
    with pytest.raises(DeliverableDoesNotExist):
        deliverables_model.delete_deliverable(EntityId("ABC-2"))
