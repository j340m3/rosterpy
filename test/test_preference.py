try:
    from .context import rosterpy
except SystemError:
    try:
        from context import rosterpy
    except ImportError:
        from rosterpy import preference, duty, driver

import datetime
import unittest


class PreferenceTest(unittest.TestCase):
    def test_init(self):
        p = preference.Preference()
        d = duty.Duty("1", "01:23:45", "23:45:00")

    def test_get_usefullness(self):
        p = preference.Preference()
        d = duty.Duty("1", "01:23:45", "23:45:00")
        self.assertEqual(p.get_usefullness(d, datetime.date(2011, 1, 2)), 0)

    def test_singleton(self):
        p = preference.Preference()
        q = preference.Preference()
        self.assertEqual(p, q)

class IllPreferenceTest(unittest.TestCase):
    def test_init(self):
        p = preference.IllPreference("15.11.2011", "18.11.2011")

    def test_get_usefullness(self):
        p = preference.IllPreference("15.11.2011", "18.11.2011")
        d = duty.Duty("1", "01:23:45", "23:45:00")
        with self.assertRaises(preference.IllException):
            p.get_usefullness(d, datetime.date(2014, 7, 22))


class RoulementPreferenceTest(unittest.TestCase):
    def setUp(self):
        self.dr = [driver.Driver("B", "A"), driver.Driver("C", "D")]
        self.du = [duty.Duty("1", "01:23:45", "23:45:00"), duty.Duty("2", "01:23:45", "23:45:00")]
        self.ro = driver.Roulement("22.07.2014", self.du, self.dr)

    def test_init(self):
        rp = preference.RoulementPreference(self.ro, self.dr)

    def test_get_usefullness(self):
        rp = preference.RoulementPreference(self.ro, self.dr)
        with self.assertRaises(preference.RoulementException):
            rp.get_usefullness(self.du[0], datetime.date(2014, 7, 22), self.dr[1])
        rp.get_usefullness(self.du[0], datetime.date(2014, 7, 22), self.dr[0])
