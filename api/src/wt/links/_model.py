from wt.ids import EntityId


class EntityLinksModel:
    def create_link(self, entity_id: EntityId, other_entity_id: EntityId):
        raise NotImplementedError()

    def delete_link(self, entity_id: EntityId, other_entity_id: EntityId):
        raise NotImplementedError()

    def delete_links(self, entity_id: EntityId):
        raise NotImplementedError()
