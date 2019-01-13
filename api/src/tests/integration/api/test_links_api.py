import pytest

from wt.common.errors import ObjectDoesNotExist
from wt.ids import EntityId, ObjectType
from wt.links import (
    InvalidLinkBetweenProjects,
    InvalidLinkToItself,
    InvalidLinkedEntities
)

ID1 = EntityId("AAA-1")
ID2 = EntityId("AAA-2")


def test_link_between_projects(links_api):
    with pytest.raises(InvalidLinkBetweenProjects):
        links_api.create_link(EntityId("AAA-1"), EntityId("BBB-1"))


def test_link_to_itself(links_api):
    with pytest.raises(InvalidLinkToItself):
        links_api.create_link(EntityId("AAA-1"), EntityId("AAA-1"))


def test_link_project_to_issue(links_api, objects_tracker_model):
    objects_tracker_model.track_object(ID1, ObjectType.project)
    objects_tracker_model.track_object(ID2, ObjectType.issue)

    with pytest.raises(InvalidLinkedEntities) as ex:
        links_api.create_link(ID1, ID2)
    assert ObjectType.project.value in ex.value.message
    assert ObjectType.issue.value in ex.value.message


def test_link_project_to_deliverable(links_api, objects_tracker_model):
    objects_tracker_model.track_object(ID1, ObjectType.project)
    objects_tracker_model.track_object(ID2, ObjectType.deliverable)

    with pytest.raises(InvalidLinkedEntities) as ex:
        links_api.create_link(ID1, ID2)
    assert ObjectType.project.value in ex.value.message
    assert ObjectType.deliverable.value in ex.value.message


def test_link_project_to_project(links_api, objects_tracker_model):
    objects_tracker_model.track_object(ID1, ObjectType.project)
    objects_tracker_model.track_object(ID2, ObjectType.project)

    with pytest.raises(InvalidLinkedEntities) as ex:
        links_api.create_link(ID1, ID2)
    assert ObjectType.project.value in ex.value.message


def test_link_deliverable_to_deliverable(links_api, objects_tracker_model):
    objects_tracker_model.track_object(ID1, ObjectType.deliverable)
    objects_tracker_model.track_object(ID2, ObjectType.deliverable)

    with pytest.raises(InvalidLinkedEntities) as ex:
        links_api.create_link(ID1, ID2)
    assert ObjectType.deliverable.value in ex.value.message


def test_link_issue_to_issue(links_api, objects_tracker_model):
    objects_tracker_model.track_object(ID1, ObjectType.issue)
    objects_tracker_model.track_object(ID2, ObjectType.issue)

    links_api.create_link(ID1, ID2)


def test_link_deliverable_to_issue(links_api, objects_tracker_model):
    objects_tracker_model.track_object(ID1, ObjectType.deliverable)
    objects_tracker_model.track_object(ID2, ObjectType.issue)

    links_api.create_link(ID1, ID2)


def test_object_does_not_exist(links_api, objects_tracker_model):
    objects_tracker_model.track_object(ID2, ObjectType.issue)

    with pytest.raises(ObjectDoesNotExist):
        links_api.create_link(ID1, ID2)


def test_other_object_does_not_exist(links_api, objects_tracker_model):
    objects_tracker_model.track_object(ID1, ObjectType.issue)

    with pytest.raises(ObjectDoesNotExist):
        links_api.create_link(ID1, ID2)
