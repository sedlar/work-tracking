class Link:
    def __init__(self, uri: str, title: str, description: str):
        self.uri = uri
        self.title = title
        self.description = description

    def __eq__(self, other):
        if isinstance(other, Link):
            return self.uri == other.uri
        return NotImplemented
