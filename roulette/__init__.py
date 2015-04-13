"""
Roulette is a library to execute flaky tests repeatedly, allowing to define arbitrary success
conditions.
"""
import functools
import time
import sys


def roll(at_most, at_least=1, success=1, delay=0, only=None, except_=None):
    """
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
    """

    def decorate(func):
        assert at_most >= at_least, "at_most must be greater or equal than at_least"
        assert not (only and except_), "only and except_ are mutually exclusive"
        assert isinstance(success, int) or (isinstance(success, float) and 0.0 <= success <= 1.0), \
            "success must be an int or a float between 0.0 and 1.0"

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            ok, last_e = 0, None
            for n in range(1, at_most + 1):
                if n >= at_least + 1 and _is_successful(success, ok, n):
                    return

                if n > 1:
                    time.sleep(delay)

                try:
                    func(*args, **kwargs)
                    ok += 1

                except Exception, e:
                    blacklisted = except_ and type(e) in except_
                    not_whitelisted = not except_ and type(e) not in (only or [AssertionError])
                    if blacklisted or not_whitelisted:
                        raise
                    last_e = e

            if not _is_successful(success, ok, n):
                raise last_e, None, sys.exc_info()[-1]

        return wrapper

    return decorate


def _is_successful(success, ok, n):
    absolute_success = isinstance(success, int) and ok >= success
    relative_success = isinstance(success, float) and ok / float(n) >= success
    return absolute_success or relative_success