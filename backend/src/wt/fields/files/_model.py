from typing import List

from wt.fields.files._obj import File


class FilesModel:
    def set_object_files(self, object_id: str, files: List[File]):
        raise NotImplementedError()

    def get_object_files(self, object_id: str) -> List[File]:
        raise NotImplementedError()
