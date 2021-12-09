import re
from typing import Any, Dict, List, Pattern, Union


class anything:
    """A matcher that's equal to anything except `None`"""

    def __eq__(self, actual: Any) -> bool:
        return actual is not None

    def __repr__(self) -> str:
        return "anything()"


class string_matching:
    """A matcher that's equal to a string matching the given pattern."""

    def __init__(self, expected: Union[str, Pattern[str]]):
        self.expected = re.compile(expected) if isinstance(expected, str) else expected

    def __eq__(self, actual: Any) -> bool:
        return isinstance(actual, str) and bool(self.expected.search(actual))

    def __repr__(self) -> str:
        return repr(self.expected.pattern)


class dict_containing:
    """A matcher that's equal to a dict that has all the keys from given dict, and their
    values are equal"""

    def __init__(self, expected: Dict):
        self.expected = expected

    def __eq__(self, actual: Any) -> bool:
        if not isinstance(actual, dict):
            return False

        for key, value in self.expected.items():
            if key not in actual or actual[key] != value:
                return False
        return True

    def __repr__(self) -> str:
        return f"dict_containing({repr(self.expected)})"


class list_containing:
    """A matcher that's equal to a list that has all the items from given list"""

    def __init__(self, expected: List):
        self.expected = expected

    def __eq__(self, actual: Any) -> bool:
        if not isinstance(actual, list):
            return False

        return all(item in actual for item in self.expected)

    def __repr__(self) -> str:
        return f"list_containing({repr(self.expected)})"
