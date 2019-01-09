from wt.objects.ids import ObjectId

PROJECT_ID1 = "PRJ"
PROJECT_ID2 = "GGG"


def test_init_counter(ids_counter_model):
    object_id = ids_counter_model.get_new_id(PROJECT_ID1)
    assert object_id == ObjectId.from_parts(PROJECT_ID1, 1)


def test_incr_counter(ids_counter_model):
    ids_counter_model.get_new_id(PROJECT_ID1)
    object_id = ids_counter_model.get_new_id(PROJECT_ID1)
    assert object_id == ObjectId.from_parts(PROJECT_ID1, 2)


def test_init_different_counter(ids_counter_model):
    ids_counter_model.get_new_id(PROJECT_ID1)
    object_id = ids_counter_model.get_new_id(PROJECT_ID2)
    assert object_id == ObjectId.from_parts(PROJECT_ID2, 1)


def test_incr_different_counter(ids_counter_model):
    ids_counter_model.get_new_id(PROJECT_ID1)
    ids_counter_model.get_new_id(PROJECT_ID2)
    object_id = ids_counter_model.get_new_id(PROJECT_ID2)
    assert object_id == ObjectId.from_parts(PROJECT_ID2, 2)
