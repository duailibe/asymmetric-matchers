import re

from asymmetric_matchers import (
    anything,
    dict_containing,
    list_containing,
    string_matching,
)


def test_string_matching():
    assert "foobarbaz" == string_matching("bar")
    assert 1 != string_matching("1")
    assert string_matching("bar") == "foobarbaz"
    assert "foobar" == string_matching(r"ba[rz]")
    assert "foobar" == string_matching(re.compile(r"ba[rz]"))


def test_dict_containing():
    assert {"foo": "bar"} == dict_containing({})
    assert {"foo": "bar"} == dict_containing({"foo": anything()})


def test_list_containing():
    assert ["foo", "bar"] == list_containing([])
    assert ["foo", "bar"] == list_containing(["foo"])
