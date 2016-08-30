try:
    from .context import rosterpy
except SystemError:
    try:
        from context import rosterpy
    except ImportError:
        from rosterpy import duty

import unittest
from datetime import timedelta


class DutyTest(unittest.TestCase):
    def test_init(self):
        d = duty.Duty("1", "01:23:45", "23:45:00")

    def test_str(self):
        d = duty.Duty("1", "01:23:45", "23:45:00")
        self.assertEqual(str(d), "Duty   1  von 01:23:45 bis 23:45:00: 22:21:15 (plus Pause:0:00:00)")

    def test_repr(self):
        d = duty.Duty("1", "01:23:45", "23:45:00")
        self.assertEqual(repr(d), "1")

    def test_get_worktime(self):
        d1 = duty.Duty("1", "00:00:00", "01:00:00")
        self.assertEqual(d1.getArbeitsdauer(), timedelta(hours=1))

        d2 = duty.Duty("1", "01:00:00", "00:00:00")
        self.assertEqual(d2.getArbeitsdauer(), timedelta(hours=23))
