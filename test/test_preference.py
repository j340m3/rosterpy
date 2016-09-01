try:
    from .context import rosterpy
except SystemError:
    try:
        from context import rosterpy
    except ImportError:
        from rosterpy import preference

import unittest


class PreferenceTest(unittest.TestCase):
    def test_init(self):
        p = preference.Preference()

class IllPreferenceTest(unittest.TestCase):
    def test_init(self):
        p = preference.IllPreference("15.11.2011", "18.11.2011")
