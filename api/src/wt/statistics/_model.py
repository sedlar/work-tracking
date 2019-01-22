from enum import Enum
from typing import List

from wt.ids import EntityId
from wt.statistics._obj import EntityStatistics


class RelationType(Enum):
    project_items = 0
    related_items = 1
    single_item = 2


class StatisticsModel:
    def get_project_ids(self, project_id: EntityId) -> List[EntityId]:
        raise NotImplementedError()

    def get_related_entities_ids(self, entity_id: EntityId) -> List[EntityId]:
        raise NotImplementedError()

    def get_entity_statistics(self, entity_ids: List[EntityId]) -> List[EntityStatistics]:
        raise NotImplementedError()
