from wt.files import File

OBJECT_ID = "PRJ-15"


def test_add_files(files_model):
    files = [File("a"), File("b")]
    files_model.set_object_files(OBJECT_ID, files)
    saved_files = files_model.get_object_files(OBJECT_ID)
    assert files == saved_files


def test_add_more_files(files_model):
    original_files = [File("a"), File("b")]
    files_model.set_object_files(OBJECT_ID, original_files)

    files = [File("a"), File("b"), File("c")]
    files_model.set_object_files(OBJECT_ID, files)

    saved_files = files_model.get_object_files(OBJECT_ID)
    assert files == saved_files


def test_remove_files(files_model):
    original_files = [File("a"), File("b")]
    files_model.set_object_files(OBJECT_ID, original_files)

    files = [File("a")]
    files_model.set_object_files(OBJECT_ID, files)

    saved_files = files_model.get_object_files(OBJECT_ID)
    assert files == saved_files


def test_add_remove_files(files_model):
    original_files = [File("a"), File("b")]
    files_model.set_object_files(OBJECT_ID, original_files)

    files = [File("b"), File("c")]
    files_model.set_object_files(OBJECT_ID, files)

    saved_files = files_model.get_object_files(OBJECT_ID)
    assert files == saved_files
