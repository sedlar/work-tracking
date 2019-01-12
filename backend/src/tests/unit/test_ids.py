from wt.entities.ids import EntityId


def test_object_id_project_id():
    assert EntityId("ABC-4").project_id == "ABC"


def test_object_id_repr():
    assert str(EntityId("EDF-89")) == "EDF-89"


def test_object_id_equals():
    assert EntityId("JJJ-55") == EntityId("JJJ-55")


def test_object_id_different_project():
    assert EntityId("AAA-33") != EntityId("AAB-33")


def test_object_id_different_object():
    assert EntityId("AAA-33") != EntityId("AAA-34")


def test_object_id_from_parts():
    assert EntityId.from_parts("UUU", 44) == EntityId("UUU-44")
