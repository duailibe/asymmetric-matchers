# asymmetric-matchers

[![CI](https://github.com/duailibe/asymmetric-matchers/actions/workflows/ci.yaml/badge.svg)](https://github.com/duailibe/asymmetric-matchers/actions/workflows/ci.yaml)
[![PyPI](https://img.shields.io/pypi/v/asymmetric-matchers)](https://pypi.org/project/asymmetric-matchers)


A collection of asymmetric matchers in Python for testing or general uses.

## What are asymmetric matchers?

An asymmetric matcher is an object that can be compared equally to a variety of other objects. Practically speaking, it's useful to test if a value satisfies a set of rules, but not an equality comparison.

Popular examples are the asymmetric matchers present in the [Jasmine](https://jasmine.github.io/) and [Jest](https://jestjs.io) (JavaScript testing frameworks.)

## Example

Say we have a function similar that calls an external API:

```python
def get_user(user_id: str, fields: List[str]) -> User:
    fields = add_default_fields(fields)
    return external_api.get_user({user_id: user_id, fields: fields})
```

And we want to write a test that asserts the `external_api.get_user()` was called with the correct arguments:

```python
def test_external_get_user_is_called():
    with mock.patch("external_api.get_user") as ext_mock:
        get_user("abc4321", ["name", "profile_picture"])
        ext_mock.assert_called_once_with("abc4321", ["name", "profile_picture"])
```

It doesn't work because we don't know what are the default fields added and perhaps the context of this specific test is not concerned on the behavior of the `add_default_fields` function. So we write more specific assertions:

```python
def test_external_get_user_is_called():
    with mock.patch("external_api.get_user") as ext_mock:
        get_user("abc4321", ["name", "profile_picture"])

        ext_mock.assert_called_once()
        args = ext_mock.call_args[0]
        assert args[0] == "abc4321"
        assert "name" in args[1]
        assert "profile_picture" in args[1]
```

Great! Now we're testing exactly what we want, but it's not as straight-forward to a future reader what exactly we want to test.

That's where an asymmetric tester is useful. We can rewrite this test as:

```python
from asymmetric_matchers import list_containing


def test_external_get_user_is_called():
    with mock.patch("external_api.get_user") as ext_mock:
        get_user("abc4321", ["name", "profile_picture"])

        ext_mock.assert_called_once_with(
            "abc4321", list_containing(["name", "profile_picture"])
        )
```

Very nice! Now it's more clear what's our intent with this test to future readers.

It's very useful in situations when we can combine two or more matchers. One example is to test that a dict contains a specific key and its value is a list that contains some elements:

```python
assert "fields" in some_dict
assert "name" in some_dict["fields"]
assert "profile_picture" in some_dict["fields"]

# using asymmetric matchers

assert some_dict == dict_containing(
    {"fields": list_containing(["name", "profile_picture"])}
)
```

## API

- **`anything()`**

  Matcher is equal to any value, except `None`.

  ```python
  plugin_mock.assert_called_once_with("app_name", anything(), True)
  ```

  It's similar to [`unittest.mock.ANY`](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.ANY).

- **`string_matching(str_or_pattern)`**

  Matcher is equal to a string that matches the pattern (using `re.search`).

  ```python
  assert generate_id() == string_matching(r"[a-z]{4}[0-9}3")
  ```

- **`list_containing(expected)`**

  Matcher is equal to a list that contains all items from `expected`.

  ```python
  assert fields == list_containing(["name", "profile_pic"])
  ```

- **`dict_containing(expected)`**

  Matcher is equal to a dict that contains all keys from `expected` and their values match.

  ```python
  assert request_dict == dict_containing({"user_id": "abc123"})
  ```

## License

[Apache-2.0 License](./LICENSE)
