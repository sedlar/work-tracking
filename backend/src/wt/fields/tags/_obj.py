from wt.fields._base_objs import FieldItem


class Tag(FieldItem):
    def __init__(self, tag: str):
        self.tag = tag

    def __eq__(self, other):
        if isinstance(other, Tag):
            return self.tag == other.tag
        return NotImplemented
