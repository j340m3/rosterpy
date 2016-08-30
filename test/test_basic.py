
try:
    from .context import rosterpy
except SystemError:
    try:
        from context import rosterpy
    except ImportError:
        from rosterpy import main

import unittest


class ImportTest(unittest.TestCase):
    def test_res(self):
        self.assertEqual(3, main.res, "As you may know, imports broken...")


if __name__ == '__main__':
    unittest.main()
