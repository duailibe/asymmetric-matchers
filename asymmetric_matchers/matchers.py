from __future__ import print_function
import re


class _base(object):
    def __ne__(self, actual):
        return not self.__eq__(actual)


class anything(_base):
    """A matcher that's equal to anything except `None`"""

    def __eq__(self, actual):
        return actual is not None

    def __ne__(self, actual):
        return not self.__eq__(actual)

    def __repr__(self):
        return "anything()"


class string_matching(_base):
    """A matcher that's equal to a string matching the given pattern."""

    def __init__(self, expected):
        self.expected = re.compile(expected) if isinstance(expected, str) else expected

    def __eq__(self, actual):
        return isinstance(actual, str) and bool(self.expected.search(actual))

    def __repr__(self):
        return repr(self.expected.pattern)


class dict_containing(_base):
    """A matcher that's equal to a dict that has all the keys from given dict, and their
    values are equal"""

    def __init__(self, expected):
        self.expected = expected

    def __eq__(self, actual):
        if not isinstance(actual, dict):
            return False

        for key, value in self.expected.items():
            if key not in actual or actual[key] != value:
                return False
        return True

    def __repr__(self):
        return "dict_containing({})".format(repr(self.expected))


class list_containing(object):
    """A matcher that's equal to a list that has all the items from given list"""

    def __init__(self, expected):
        self.expected = expected

    def __eq__(self, actual):
        if not isinstance(actual, list):
            return False

        return all(item in actual for item in self.expected)

    def __repr__(self):
        return "list_containing({})".format(repr(self.expected))
