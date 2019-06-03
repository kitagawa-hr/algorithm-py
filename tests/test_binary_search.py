import unittest
import random

from src import binary_search


class TestBinarySearch(unittest.TestCase):
    def test_binary_search(self):
        for _ in range(5):
            N = 10000
            solution = random.randint(0, N)

            def condition(n):
                return n >= solution

            self.assertEqual(
                binary_search.binary_search(
                    condition=condition, initial_left=0, initial_right=N
                ),
                solution,
            )

    def test_binary_search_no_solution(self):
        def condition(n):
            return n >= 200

        self.assertIsNone(
            binary_search.binary_search(
                condition=condition, initial_left=0, initial_right=100
            )
        )

    def test_binary_search_all_true(self):
        def condition(n):
            return True

        right = random.randint(0, 1000)
        self.assertEqual(
            binary_search.binary_search(
                condition=condition, initial_left=0, initial_right=right
            ),
            0,
        )
