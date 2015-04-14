Roullete
========

Roulette is a small utility to run flaky tests - like integration tests that rely on external services that might be 
temporarily unavailable, etc. 
It provides a decorator that you can use in your tests so they run until some exit criteria is met.

It also can be used to run tests many times to help to detect concurrency issues.



### Usage.

```python
from roulette import roll

@roll(3)  # runs the test up to 3 times, ends successfully if one execution succeeds
def test_something(self):
    ...


@roll(3, delay=5)  # same as before, but waits 5 seconds between executions
def test_something(self):
    ...


@roll(3, success=2)  # runs the test up to 3 times, requiring 2 successful executions to pass
def test_something(self):
    ...


@roll(10, success=0.5)  # runs the test up to 10 times, requiring half of the executions to be successful in order to pass
def test_something(self):
    ...


@roll(10, at_least=4, success=0.5)  # same as before, but forcing 4 executions before exiting
def test_something(self):
    ...

```

All the cases above just "swallow" and retry upon `AssertionError`s. It is also possible to either whitelist or 
blacklist a custom list of exception types. Any blacklisted or not whitelisted exception type will cause the test to
fail without executing it more times

```python
from roulette import roll


@roll(3, only=[AssertionError, AttributeError])  # retries on any AssertionError or AttributeError
def test_something(self):
    ...

@roll(3, except_=[KeyError])  # retries on all exception types except KeyError
def test_something(self):
    ...
```


### Reference.

    :param at_most (int): Maximum number of times to execute the test.

    :param at_least (int): Minimum number of times to execute the test.
    [DEFAULT = 1]

    :param success (int|float): Threshold which defines a successful test.
    If `success` is an <int> i, the test will be marked as successful when i repetitions are
    successful.
    If `success` is a <float> f between 0.0 and 1.0, the test will be considered successful when
    the number of successful repetitions / number of total repetitions is >= f.

    The test must run `at_least` times before it can be considered successful or `at_most` times
    before it can be considered failed.
    [DEFAULT = 1]

    :param delay (int): Number of seconds to wait between repetitions.
    [DEFAULT = 0]

    :param only (list): Whitelist of exceptions which, if raised by the test, won't mark the test
    as failed. Any exception not whitelisted will cause the test to fail immediately regardless
    the `at_least` settings
    [DEFAULT = ASSERTION_ERROR]

    :param except_ (list): Blacklist of exceptions which, if raised by the test, will mark the test
    as failed regardless the `at_least` settings. Any exception not blacklisted will be swallowed
    and the test might be repeated according to the `at_most` settings.
    [DEFAULT = None]

    `only` and `expect_` are mutually exclusive, only one can be supplied.

