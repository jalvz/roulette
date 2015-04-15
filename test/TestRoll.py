import functools
from unittest2 import TestCase
from roulette import roll


def _fail_attribute():
    raise AttributeError


def fibo_gen(n=1, m=1):
    while True:
        yield n
        aux = n + m
        n = m
        m = aux


def meta_test(stop_at=None, exc_type=None):
    def decorate(func):
        @functools.wraps(func)
        def wrapper(this, *args, **kwargs):
            try:
                func(this, *args, **kwargs)
                assert exc_type is None, "Exception not raised {}".format(exc_type)
            except Exception, e:
                assert isinstance(e, exc_type), "Unexpected exception raised {}".format(type(e))

            nx = this.next()
            assert stop_at == nx, \
                "Next element in sequence does not match {} != {}".format(stop_at, nx)
        return wrapper
    return decorate


class TestRoll(TestCase):

    def setUp(self):
        self.fibo = fibo_gen()
        self.next = self.fibo.next
        # 1, 1, 2, 3, 5, 8, 13, 21, 34...

    @meta_test(1)
    @roll(3, success=1)
    def test_simple(self):
        self.assertGreater(self.next(), 0)

    @meta_test(13)
    @roll(8, success=3)
    def test_success_int(self):
        self.assertGreater(self.next(), 2)

    @meta_test(5, AssertionError)
    @roll(4, success=1)
    def test_fail_int(self):
        self.assertEqual(self.next(), 5)

    @meta_test(34)
    @roll(8, success=0.5)
    def test_success_float(self):
        self.assertGreater(self.next(), 4)

    @meta_test(34, AssertionError)
    @roll(8, success=0.51)
    def test_fail_float(self):
        self.assertGreater(self.next(), 4)

    @meta_test(13)
    @roll(8, success=3)
    def test_success_int(self):
        self.assertGreater(self.next(), 2)

    @meta_test(3)
    @roll(3, success=1, only=[AttributeError, AssertionError])
    def test_only_pass(self):
        if self.next() == 1:
            raise AttributeError

    @meta_test(1, AttributeError)
    @roll(3, success=1)
    def test_only_fail(self):
        if self.next() == 1:
            raise AttributeError

    @meta_test(3)
    @roll(3, success=1, except_=[KeyError])
    def test_except_pass(self):
        if self.next() == 1:
            raise AttributeError

    @meta_test(1, AttributeError)
    @roll(3, success=1, except_=[AttributeError])
    def test_except_fail(self):
        if self.next() == 1:
            raise AttributeError

    @meta_test(8)
    @roll(10, success=1, at_least=5)
    def test_at_least(self):
        self.assertGreater(self.next(), 0)
