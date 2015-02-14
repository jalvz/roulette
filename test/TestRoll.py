import random
from unittest2 import TestCase
from roulette import roll


class TestRoll(TestCase):

    @roll(10)
    def test_sum(self):
        self.assertEqual(1 + 2, 3)

    @roll(10)
    def test_rand(self):
        self.assertGreater(random.randint(0, 20), 2)