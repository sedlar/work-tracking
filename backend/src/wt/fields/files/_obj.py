class File:
    def __init__(self, uri):
        self.uri = uri

    def __eq__(self, other):
        if isinstance(other, File):
            return self.uri == other.uri
        return NotImplemented
