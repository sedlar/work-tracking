from typing import List
from wt.fields.links._obj import Link


class LinkSerializer:
    @staticmethod
    def serialize_link(link: Link) -> dict:
        return {
            "uri": link.uri,
            "title": link.title,
            "description": link.description,
        }

    def serialize_links(self, links: List[Link]):
        return [
            self.serialize_link(link)
            for link in links
        ]


class LinkDeserializer:
    @staticmethod
    def deserialize_link(link: dict) -> Link:
        return Link(
            uri=link["uri"],
            title=link["title"],
            description=link["description"],
        )

    def deserialize_links(self, links):
        return [
            self.deserialize_link(link)
            for link
            in links
        ]
