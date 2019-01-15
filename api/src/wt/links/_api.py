from wt.ids import EntityId, ObjectsTrackerModel, EntityType
from wt.links._errors import InvalidLinkedEntities, InvalidLinkToItself, InvalidLinkBetweenProjects
from wt.links._model import EntityLinksModel
from wt.common.errors import ObjectDoesNotExist


class EntityLinksApi:
    _valid_link_types = [
        {EntityType.issue},
        {EntityType.issue, EntityType.deliverable},
    ]

    def __init__(
            self,
            entity_links_model: EntityLinksModel,
            objects_tracker_model: ObjectsTrackerModel
    ):
        self._entity_links_model = entity_links_model
        self._objects_tracker_model = objects_tracker_model

    def create_link(self, entity_id: EntityId, other_entity_id: EntityId):
        self._check_link(entity_id, other_entity_id)
        self._entity_links_model.create_link(entity_id, other_entity_id)

    def delete_link(self, entity_id: EntityId, other_entity_id: EntityId):
        self._entity_links_model.delete_link(entity_id, other_entity_id)

    def _check_link(self, entity_id, other_entity_id):
        if entity_id == other_entity_id:
            raise InvalidLinkToItself()

        if entity_id.project_id != other_entity_id.project_id:
            raise InvalidLinkBetweenProjects()

        object_types = self._objects_tracker_model.get_objects_types([entity_id, other_entity_id])
        if entity_id not in object_types:
            raise ObjectDoesNotExist("Object", entity_id)

        if other_entity_id not in object_types:
            raise ObjectDoesNotExist("Object", other_entity_id)

        if {object_types[entity_id], object_types[other_entity_id]} not in self._valid_link_types:
            raise InvalidLinkedEntities(object_types[entity_id], object_types[other_entity_id])
