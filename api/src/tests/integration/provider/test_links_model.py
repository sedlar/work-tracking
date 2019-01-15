import pytest
from wt.ids import EntityId, EntityType
from wt.links import LinkAlreadyExists, LinkDoesNotExist


ID1 = EntityId("ABC-1")
ID2 = EntityId("ABC-2")
ID3 = EntityId("ABC-3")

def test_add_link(entity_links_model, objects_tracker_model):
    objects_tracker_model.track_object(ID1, EntityType.issue)
    objects_tracker_model.track_object(ID2, EntityType.issue)

    entity_links_model.create_link(ID1, ID2)

    with pytest.raises(LinkAlreadyExists):
        entity_links_model.create_link(ID1, ID2)


def test_add_reversed_link(entity_links_model, objects_tracker_model):
    objects_tracker_model.track_object(ID1, EntityType.issue)
    objects_tracker_model.track_object(ID2, EntityType.issue)

    entity_links_model.create_link(ID1, ID2)

    with pytest.raises(LinkAlreadyExists):
        entity_links_model.create_link(ID2, ID1)


def test_remove_link(entity_links_model, objects_tracker_model):
    objects_tracker_model.track_object(ID1, EntityType.issue)
    objects_tracker_model.track_object(ID2, EntityType.issue)

    entity_links_model.create_link(ID1, ID2)
    entity_links_model.delete_link(ID1, ID2)
    entity_links_model.create_link(ID1, ID2)


def test_remove_reversed_link(entity_links_model, objects_tracker_model):
    objects_tracker_model.track_object(ID1, EntityType.issue)
    objects_tracker_model.track_object(ID2, EntityType.issue)

    entity_links_model.create_link(ID1, ID2)
    entity_links_model.delete_link(ID2, ID1)
    entity_links_model.create_link(ID1, ID2)


def test_remove_links(entity_links_model, objects_tracker_model):
    objects_tracker_model.track_object(ID1, EntityType.issue)
    objects_tracker_model.track_object(ID2, EntityType.issue)
    objects_tracker_model.track_object(ID3, EntityType.issue)

    entity_links_model.create_link(ID1, ID2)
    entity_links_model.create_link(ID1, ID3)
    entity_links_model.delete_links(ID1)

    entity_links_model.create_link(ID1, ID2)
    entity_links_model.create_link(ID1, ID3)


def test_remove_missing_link(entity_links_model):
    with pytest.raises(LinkDoesNotExist):
        entity_links_model.delete_link(ID1, ID2)


def test_remove_one_of_many_links(entity_links_model, objects_tracker_model):
    objects_tracker_model.track_object(ID1, EntityType.issue)
    objects_tracker_model.track_object(ID2, EntityType.issue)
    objects_tracker_model.track_object(ID3, EntityType.issue)

    entity_links_model.create_link(ID1, ID2)
    entity_links_model.create_link(ID1, ID3)
    entity_links_model.delete_links(ID2)

    entity_links_model.create_link(ID1, ID2)
    with pytest.raises(LinkAlreadyExists):
        entity_links_model.create_link(ID1, ID3)
