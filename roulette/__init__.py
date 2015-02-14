"""
Library to execute tests repeatedly and define success criteria.
"""
import functools


def roll(times, delay=0, success=0.66, until_success=True, only=[AssertionError], except_=None):
    """
    :param times (int): Maximum number of times to execute the test.
    :param delay (int): Number of seconds to wait between repetitions.
    :param success: Criteria which defines a successful test. If `success` is an <int> i, the test
    will be considered successful when i repetitions are successful.
    If `success` is a <float> f between 0.0 and 1.0, the test will be considered successful when
    the number of successful repetitions / number of total repetitions is >= f.
    :param until_success (bool): If true, it will stop executing the test when success condition
    is met.
    :param only (list): Whitelist of exceptions that can throw the test which will cause repeated
    executions according to `times` and `until_success` arguments.
    If `except_` is specified, only must be None.
    :param except_ (list): Blacklist of exceptions that can throw the test which will mark test as
    failed regardless any other settings.
    If `only` is specified, expect_ must be None.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                func(*args, **kwargs)
        return wrapper
    return decorator
