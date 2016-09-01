try:
    from .context import rosterpy
except SystemError:
    try:
        from context import rosterpy
    except ImportError:
        from rosterpy import preference, duty

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

class IllPreferenceTest(unittest.TestCase):
    def test_init(self):
        p = preference.IllPreference("15.11.2011", "18.11.2011")
