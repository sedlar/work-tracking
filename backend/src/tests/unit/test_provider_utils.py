from wt.provider.db._utils import get_enum_length
from enum import Enum


def test_enum_length():
    class A(Enum):
        a = "a"
        bb = "bb"
    assert get_enum_length(A) == 2