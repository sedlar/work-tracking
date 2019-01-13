import pytest

from wt.fields.files import File, DuplicateFileReceived
from wt.ids import EntityId

OBJECT_ID = EntityId("PRJ-15")


def test_add_files(files_model):
    files = [File("a"), File("b")]
    files_model.set_entity_files(OBJECT_ID, files)
    saved_files = files_model.get_entity_files(OBJECT_ID)
    assert files == saved_files


def test_add_more_files(files_model):
    original_files = [File("a"), File("b")]
    files_model.set_entity_files(OBJECT_ID, original_files)

    files = [File("a"), File("b"), File("c")]
    files_model.set_entity_files(OBJECT_ID, files)

    saved_files = files_model.get_entity_files(OBJECT_ID)
    assert files == saved_files


def test_remove_files(files_model):
    original_files = [File("a"), File("b")]
    files_model.set_entity_files(OBJECT_ID, original_files)

    files = [File("a")]
    files_model.set_entity_files(OBJECT_ID, files)

    saved_files = files_model.get_entity_files(OBJECT_ID)
    assert files == saved_files


def test_add_remove_files(files_model):
    original_files = [File("a"), File("b")]
    files_model.set_entity_files(OBJECT_ID, original_files)

    files = [File("b"), File("c")]
    files_model.set_entity_files(OBJECT_ID, files)

    saved_files = files_model.get_entity_files(OBJECT_ID)
    assert files == saved_files


def test_duplicate_files(files_model):
    files = [File("a"), File("a")]
    with pytest.raises(DuplicateFileReceived):
        files_model.set_entity_files(OBJECT_ID, files)
