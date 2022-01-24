import collections
import re

from asymmetric_matchers import (
    anything,
    any as any_,
    string_matching,
    list_containing,
    dict_containing,
)


def test_anything():
    assert 0 == anything()
    assert "" == anything()
    assert [] == anything()
    assert {} == anything()
    assert None != anything()  # noqa: E711


def test_any():
    assert 0 == any_(int)
    assert "" == any_(str)


def test_string_matching():
    assert "foobarbaz" == string_matching("bar")
    assert "string" != string_matching("bar")

    assert 1 != string_matching("1")
    assert string_matching("bar") == "foobarbaz"

    assert "foobar" == string_matching(r"ba[rz]")
    assert "foobar" == string_matching(re.compile(r"ba[rz]"))

    assert repr(string_matching("foo")) == "'foo'"
    assert repr(string_matching(re.compile(r"foo"))) == "'foo'"


def test_dict_containing():
    assert {"foo": "bar"} == dict_containing({})
    assert {"foo": "bar"} == dict_containing({"foo": anything()})
    assert {"notfoo": "bar"} != dict_containing({"foo": anything()})
    assert dict_containing({"foo": "bar"}) == dict_containing({"foo": "bar"})
    assert repr(dict_containing({"foo": "bar"})) == "dict_containing({'foo': 'bar'})"

    assert dict_containing({"foo": "bar"}) != {"foo"}

    assert collections.Counter(foo=4) == dict_containing({"foo": anything()})


def test_list_containing():
    assert ["foo", "bar"] == list_containing([])
    assert ["foo", "bar"] == list_containing(["foo"])
    assert ["notfoo", "bar"] != list_containing(["foo"])
    assert list_containing(["foo", "bar"]) == list_containing(["bar", "foo"])
    assert repr(list_containing(["foo", "bar"])) == "list_containing(['foo', 'bar'])"

    assert {"foo"} != list_containing(["foo"])

    assert ["foo", [], "bar"] == list_containing([[]])
    assert ["foo", [], "bar"] == list_containing(["foo"])
