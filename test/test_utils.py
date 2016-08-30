try:
    from .context import rosterpy
except SystemError:
    try:
        from context import rosterpy
    except ImportError:
        from rosterpy import utils

import unittest


class UtilsTest(unittest.TestCase):
    def test_pairwise(self):
        self.assertEqual(list(utils.pairwise(range(3))), [(0, 1), (1, 2)])


if __name__ == '__main__':
    unittest.main()
