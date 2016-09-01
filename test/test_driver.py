try:
    from .context import rosterpy
except SystemError:
    try:
        from context import rosterpy
    except ImportError:
        from rosterpy import driver

import unittest


class DriverTest(unittest.TestCase):
    def test_init(self):
        d = driver.Driver("B", "A")
        self.assertEqual(d.nachname, "B")
        self.assertEqual(d.vorname, "A")


class RoulementDriverTest(unittest.TestCase):
    def test_init(self):
        d = driver.RoulementDriver("B", "A")
        self.assertEqual(d.nachname, "B")
        self.assertEqual(d.vorname, "A")
