class Link:
    def __init__(self, uri: str, name: str, description: str):
        self.uri = uri
        self.name = name
        self.description = description

    def __eq__(self, other):
        if isinstance(other, Link):
            return self.uri == other.uri
        return NotImplemented
