import re


class _base(object):
    def __ne__(self, actual):
        return not self.__eq__(actual)


class anything(_base):
    """A matcher that's equal to anything except `None`"""

    def __eq__(self, actual):
        return actual is not None

    def __repr__(self):
        return "anything()"  # pragma: no cover


class any(_base):
    def __init__(self, *expected):
        self.expected = tuple(expected)

    def __eq__(self, actual):
        return isinstance(actual, self.expected)

    def __repr__(self):
        return "any({!r})".format(self.expected)  # pragma: no cover


class string_matching(_base):
    """Matches a string containing another

    "Python" == string_matching("Py")
    """

    def __init__(self, expected):
        self.expected = re.compile(expected) if isinstance(expected, str) else expected

    def __eq__(self, actual):
        return isinstance(actual, str) and bool(self.expected.search(actual))

    def __repr__(self):
        return repr(self.expected.pattern)


class dict_containing(_base, dict):
    """Matches a dict that contas the passed keys and matches their values

    {"user_id": "123", "first_name": "John"} == dict_containing({"user_id": "123"})
    """

    def __eq__(self, actual):
        if not isinstance(actual, dict):
            return False

        for key, value in self.items():
            if key not in actual or actual[key] != value:
                return False
        return True

    def __repr__(self):
        return "dict_containing({})".format(super(dict_containing, self).__repr__())


class list_containing(_base, list):
    """Matches a list that contains the passed values

    [0, 1, 2, 3, 4] == list_containing([4, 2])
    """

    def __eq__(self, actual):
        if not isinstance(actual, list):
            return False

        return all(item in actual for item in self)

    def __repr__(self):
        return "list_containing({})".format(super(list_containing, self).__repr__())
