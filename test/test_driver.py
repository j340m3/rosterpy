try:
    from .context import rosterpy
except SystemError:
    try:
        from context import rosterpy
    except ImportError:
        from rosterpy import driver, duty, preference

import unittest

class DriverTest(unittest.TestCase):
    def test_init(self):
        d = driver.Driver("B", "A")
        self.assertEqual(d.nachname, "B")
        self.assertEqual(d.vorname, "A")

    def test_preference(self):
        p1 = preference.Preference()
        with self.assertRaises(AttributeError):
            d = driver.Driver("B", "A", [p1])

        p2 = preference.IllPreference("15.11.2011", "18.11.2011")
        d = driver.Driver("B", "A", [p2])

class RoulementTest(unittest.TestCase):
    def test_init(self):
        d = driver.Roulement(6, "22.07.2014")
