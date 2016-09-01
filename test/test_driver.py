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

    def test_get_preference(self):
        p = preference.IllPreference("15.11.2011", "18.11.2011")
        d = driver.Driver("B", "A", [p])
        self.assertIn(p, d.getPreference("16.11.2011"))
        self.assertEqual(preference.Preference(), d.getPreference("16.11.2012"))

    def test_repr(self):
        d = driver.Driver("B", "A")
        self.assertEqual(d.__repr__(), "Driver B, A")

class RoulementTest(unittest.TestCase):
    def test_init(self):
        du = duty.Duty("1", "01:23:45", "23:45:00")
        dr = driver.Roulement("22.07.2014", [du])

    def test_bind(self):
        d1 = driver.Driver("B", "A")
        d2 = driver.Driver("C", "D")
        du = duty.Duty("1", "01:23:45", "23:45:00")
        dr = driver.Roulement("22.07.2014", [du])
        dr.bind(d1, 0)
        dr.bind(d1, 0)
        with self.assertRaises(driver.InvalidRoulementPositionException):
            dr.bind(d1, 1)
        with self.assertRaises(driver.RoulementPositionAlreadyAssignedException):
            dr.bind(d2, 0)
        dr2 = driver.Roulement("01.02.1993", [duty.Duty("2", "01:23:45", "23:45:00")])
        with self.assertRaises(driver.RoulementDriverAlreadyAssignedException):
            dr2.bind(d1, 0)

    def test_unbind(self):
        d1 = driver.Driver("B", "A")
        d2 = driver.Driver("C", "D")
        du = duty.Duty("1", "01:23:45", "23:45:00")
        dr = driver.Roulement("22.07.2014", [du])
        dr.bind(d1, 0)
        self.assertEqual(d1.roulement, dr)
        self.assertIn(d1, dr._driver.values())
        dr.unbind(d1)
        self.assertEqual(d1.roulement, None)
        self.assertNotIn(d1, dr._driver.values())


class DriverInstanceManagerTest(unittest.TestCase):
    def test_init(self):
        d = driver.DriverInstanceManager()
        d1 = driver.Driver("B", "A")
        d2 = driver.Driver("C", "D")
        d.add(d1)
        d.add(d2)
        for i, dr in enumerate(d):
            self.assertEqual(d.getAll()[i], dr)

    def test_import_json(self):
        dim = driver.DriverInstanceManager()
        try:
            dim.import_drivers("test/driver.json")
        except OSError:
            dim.import_drivers("driver.json")
        with self.assertRaises(duty.FileEndingNotKnownException):
            dim.import_drivers("ngfunlegf.glnveflng")

    def test_import_xml(self):
        dim = driver.DriverInstanceManager()
        try:
            dim.import_drivers("test/driver.xml")
        except OSError:
            dim.import_drivers("driver.xml")
