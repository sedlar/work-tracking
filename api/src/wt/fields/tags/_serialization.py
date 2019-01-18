from typing import List
from wt.fields.tags._obj import Tag


class TagsSerializer:
    @staticmethod
    def serialize_tag(tag: Tag) -> str:
        return tag.tag

    def serialize_tags(self, tags: List[Tag]):
        return [
            self.serialize_tag(tag)
            for tag in tags
        ]


class TagsDeserializer:
    @staticmethod
    def deserialize_tag(tag: str) -> Tag:
        return Tag(tag)

    def deserialize_tags(self, tags):
        return [
            self.deserialize_tag(tag)
            for tag
            in tags
        ]
