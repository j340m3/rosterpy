try:
    from .context import rosterpy
except SystemError:
    try:
        from context import rosterpy
    except ImportError:
        from rosterpy import roster
import unittest


class SchoolTimeCalendarTest(unittest.TestCase):
    def test_is_schooltime(self):
        a = roster.Schulzeitenkalender()
        self.assertEqual(a.isSchulzeit(4), False)
