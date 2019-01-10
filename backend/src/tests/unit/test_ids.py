from wt.objects.ids import ObjectId


def test_object_id_project_id():
    assert ObjectId("ABC-4").project_id == "ABC"


def test_object_id_repr():
    assert str(ObjectId("EDF-89")) == "EDF-89"


def test_object_id_equals():
    assert ObjectId("JJJ-55") == ObjectId("JJJ-55")


def test_object_id_different_project():
    assert ObjectId("AAA-33") != ObjectId("AAB-33")


def test_object_id_different_object():
    assert ObjectId("AAA-33") != ObjectId("AAA-34")


def test_object_id_from_parts():
    assert ObjectId.from_parts("UUU", 44) == ObjectId("UUU-44")
