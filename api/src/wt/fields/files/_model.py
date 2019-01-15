from typing import List

from wt.ids import BaseId
from wt.fields.files._obj import File


class FilesModel:
    def set_entity_files(self, entity_id: BaseId, files: List[File]):
        raise NotImplementedError()

    def get_entity_files(self, entity_id: BaseId) -> List[File]:
        raise NotImplementedError()
