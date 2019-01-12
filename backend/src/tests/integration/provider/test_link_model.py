import pytest

from tests.integration.factories.objs import create_link
from wt.fields.links import DuplicateLinkReceived

OBJECT_ID = "PRJ-15"


def test_add_links(links_model):
    links = [create_link("a"), create_link("b")]
    links_model.set_object_links(OBJECT_ID, links)
    saved_links = links_model.get_object_links(OBJECT_ID)
    assert links == saved_links


def test_add_more_links(links_model):
    original_links = [create_link("a"), create_link("b")]
    links_model.set_object_links(OBJECT_ID, original_links)

    links = [create_link("a"), create_link("b"), create_link("c")]
    links_model.set_object_links(OBJECT_ID, links)

    saved_links = links_model.get_object_links(OBJECT_ID)
    assert links == saved_links


def test_remove_links(links_model):
    original_links = [create_link("a"), create_link("b")]
    links_model.set_object_links(OBJECT_ID, original_links)

    links = [create_link("a")]
    links_model.set_object_links(OBJECT_ID, links)

    saved_links = links_model.get_object_links(OBJECT_ID)
    assert links == saved_links


def test_add_remove_links(links_model):
    original_links = [create_link("a"), create_link("b")]
    links_model.set_object_links(OBJECT_ID, original_links)

    links = [create_link("b"), create_link("c")]
    links_model.set_object_links(OBJECT_ID, links)

    saved_links = links_model.get_object_links(OBJECT_ID)
    assert links == saved_links


def test_duplicate_links(links_model):
    links = [create_link("a"), create_link("a")]
    with pytest.raises(DuplicateLinkReceived):
        links_model.set_object_links(OBJECT_ID, links)
