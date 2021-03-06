import pytest

from wt.fields.tags import Tag, DuplicateTagReceived
from wt.ids import EntityId

OBJECT_ID = EntityId("PRJ-15")


def test_add_tags(tags_model):
    tags = [Tag("a"), Tag("b")]
    tags_model.set_entity_tags(OBJECT_ID, tags)
    saved_tags = tags_model.get_entity_tags(OBJECT_ID)
    assert tags == saved_tags


def test_add_more_tags(tags_model):
    original_tags = [Tag("a"), Tag("b")]
    tags_model.set_entity_tags(OBJECT_ID, original_tags)

    tags = [Tag("a"), Tag("b"), Tag("c")]
    tags_model.set_entity_tags(OBJECT_ID, tags)

    saved_tags = tags_model.get_entity_tags(OBJECT_ID)
    assert tags == saved_tags


def test_remove_tags(tags_model):
    original_tags = [Tag("a"), Tag("b")]
    tags_model.set_entity_tags(OBJECT_ID, original_tags)

    tags = [Tag("a")]
    tags_model.set_entity_tags(OBJECT_ID, tags)

    saved_tags = tags_model.get_entity_tags(OBJECT_ID)
    assert tags == saved_tags


def test_add_remove_tags(tags_model):
    original_tags = [Tag("a"), Tag("b")]
    tags_model.set_entity_tags(OBJECT_ID, original_tags)

    tags = [Tag("b"), Tag("c")]
    tags_model.set_entity_tags(OBJECT_ID, tags)

    saved_tags = tags_model.get_entity_tags(OBJECT_ID)
    assert tags == saved_tags


def test_duplicate_tags(tags_model):
    tags = [Tag("a"), Tag("a")]
    with pytest.raises(DuplicateTagReceived):
        tags_model.set_entity_tags(OBJECT_ID, tags)
