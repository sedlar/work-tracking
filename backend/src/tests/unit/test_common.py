from wt.common import remove_nones


def test_remove_nones_empty():
    assert remove_nones({}) == {}


def test_remove_nones_flat():
    before = {
            "A": "A",
            "B": None,
            "C": "",
            "D": 0,
        }
    after = {
               "A": "A",
               "C": "",
               "D": 0,
           }
    assert remove_nones(before) == after


def test_remove_nones_nested():
    before = {
        "A": "A",
        "B": None,
        "C": "",
        "D": 0,
        "E": {
            "A": "A",
            "B": None,
            "C": "",
            "D": 0,
        }
    }
    after = {
        "A": "A",
        "C": "",
        "D": 0,
        "E": {
            "A": "A",
            "C": "",
            "D": 0,
        }
    }
    assert remove_nones(before) == after
