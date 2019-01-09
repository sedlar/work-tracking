from wt.objects.ids import ObjectId, ObjectType, ObjectsDoesNotExist
from tests.integration.factories.objs import create_project
import pytest

OBJECT_ID1 = "PRJ-23"
OBJECT_ID2 = "GGG-56"


def test_track_object(objects_tracker_model, put_project):
    object_id = ObjectId(OBJECT_ID1)
    put_project(create_project(object_id.project_id))

    objects_tracker_model.track_object(object_id, ObjectType.deliverable)

    assert objects_tracker_model.get_objects_types([object_id]) == {
        object_id: ObjectType.deliverable
    }


def test_untrack_object(objects_tracker_model, put_project):
    object_id = ObjectId(OBJECT_ID1)
    put_project(create_project(object_id.project_id))

    objects_tracker_model.track_object(object_id, ObjectType.deliverable)
    objects_tracker_model.untrack_object(object_id)

    with pytest.raises(ObjectsDoesNotExist):
        objects_tracker_model.get_objects_types([object_id])


def test_get_multiple_object_types(objects_tracker_model, put_project):
    object_id1 = ObjectId(OBJECT_ID1)
    object_id2 = ObjectId(OBJECT_ID2)
    put_project(create_project(object_id1.project_id))
    put_project(create_project(object_id2.project_id))

    objects_tracker_model.track_object(object_id1, ObjectType.deliverable)
    objects_tracker_model.track_object(object_id2, ObjectType.issue)

    assert objects_tracker_model.get_objects_types([object_id1, object_id2]) == {
        object_id1: ObjectType.deliverable,
        object_id2: ObjectType.issue,
    }


def test_get_one_of_multiple_object_types(objects_tracker_model, put_project):
    object_id1 = ObjectId(OBJECT_ID1)
    object_id2 = ObjectId(OBJECT_ID2)
    put_project(create_project(object_id1.project_id))
    put_project(create_project(object_id2.project_id))

    objects_tracker_model.track_object(object_id1, ObjectType.deliverable)
    objects_tracker_model.track_object(object_id2, ObjectType.issue)

    assert objects_tracker_model.get_objects_types([object_id2]) == {
        object_id2: ObjectType.issue,
    }


def test_get_object_type(objects_tracker_model, put_project):
    object_id1 = ObjectId(OBJECT_ID1)
    put_project(create_project(object_id1.project_id))

    objects_tracker_model.track_object(object_id1, ObjectType.deliverable)

    assert objects_tracker_model.get_object_type(object_id1) == ObjectType.deliverable


def test_get_missing_objects(objects_tracker_model):
    with pytest.raises(ObjectsDoesNotExist):
        objects_tracker_model.get_objects_types([ObjectId(OBJECT_ID1)])


def test_get_missing_object(objects_tracker_model):
    with pytest.raises(ObjectsDoesNotExist):
        objects_tracker_model.get_object_type(ObjectId(OBJECT_ID1))
