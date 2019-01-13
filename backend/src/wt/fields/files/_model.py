from typing import List

from wt.ids import EntityId
from wt.fields.files._obj import File


class FilesModel:
    def set_entity_files(self, entity_id: EntityId, files: List[File]):
        raise NotImplementedError()

    def get_entity_files(self, entity_id: EntityId) -> List[File]:
        raise NotImplementedError()
