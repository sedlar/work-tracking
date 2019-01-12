from wt.entities.ids import EntityId

PROJECT_ID1 = EntityId("PRJ")
PROJECT_ID2 = EntityId("GGG")


def test_init_counter(ids_counter_model):
    object_id = ids_counter_model.get_new_id(PROJECT_ID1)
    assert object_id == EntityId.from_parts(PROJECT_ID1.project_id, 1)


def test_incr_counter(ids_counter_model):
    ids_counter_model.get_new_id(PROJECT_ID1)
    object_id = ids_counter_model.get_new_id(PROJECT_ID1)
    assert object_id == EntityId.from_parts(PROJECT_ID1.project_id, 2)


def test_init_different_counter(ids_counter_model):
    ids_counter_model.get_new_id(PROJECT_ID1)
    object_id = ids_counter_model.get_new_id(PROJECT_ID2)
    assert object_id == EntityId.from_parts(PROJECT_ID2.project_id, 1)


def test_incr_different_counter(ids_counter_model):
    ids_counter_model.get_new_id(PROJECT_ID1)
    ids_counter_model.get_new_id(PROJECT_ID2)
    object_id = ids_counter_model.get_new_id(PROJECT_ID2)
    assert object_id == EntityId.from_parts(PROJECT_ID2.project_id, 2)


def test_drop_project(ids_counter_model):
    ids_counter_model.get_new_id(PROJECT_ID1)
    ids_counter_model.drop_project(PROJECT_ID1)
    object_id = ids_counter_model.get_new_id(PROJECT_ID1)
    assert object_id == EntityId.from_parts(PROJECT_ID1.project_id, 1)
