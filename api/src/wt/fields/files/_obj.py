class File:
    def __init__(self, uri: str):
        self.uri = uri

    def __eq__(self, other):
        if isinstance(other, File):
            return self.uri == other.uri
        return NotImplemented
