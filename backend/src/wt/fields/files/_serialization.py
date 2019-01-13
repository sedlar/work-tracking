from typing import List
from wt.fields.files._obj import File


class FileSerializer:
    @staticmethod
    def serialize_file(file: File):
        return file.uri

    def serialize_files(self, files: List[File]):
        return [
            self.serialize_file(file)
            for file in files
        ]


class FileDeserializer:
    @staticmethod
    def deserialize_file(file) -> File:
        return File(file)

    def deserialize_files(self, files):
        return [
            self.deserialize_file(file)
            for file
            in files
        ]
