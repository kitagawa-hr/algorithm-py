import unittest

from src import two_pointers


class TestTwoPointers(unittest.TestCase):
    def test_solve_abc032_c(self):
        test_cases = [
            (6, [4, 3, 1, 1, 2, 10, 2], 4),
            (10, [10, 10, 10, 10, 0, 10], 6),
            (9, [10, 10, 10, 10, 10, 10], 0),
            (0, [1, 2, 3, 4], 0),
        ]
        for k, s, ans in test_cases:
            self.assertEqual(ans, two_pointers.solve_abc032_c(s, k))
