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

        d3 = duty.Duty("1", "14:00:00", "01:00:00")
        self.assertEqual(d3.getArbeitsdauer(), timedelta(hours=11))

    def test_get_pause(self):
        d = duty.Duty("1", "01:00:00", "00:00:00")
        self.assertEqual(d.getPause(), timedelta())


class CoupeTest(unittest.TestCase):
    def test_init(self):
        d1 = duty.Duty("1", "09:00:00", "11:00:00")
        d2 = duty.Duty("1", "13:00:00", "16:00:00")
        c1 = duty.Coupe(d1, d2)

    def test_get_worktime(self):
        d1 = duty.Duty("1", "09:00:00", "11:00:00")
        d2 = duty.Duty("1", "13:00:00", "16:00:00")
        c1 = duty.Coupe(d1, d2)
        self.assertEqual(c1.getArbeitsdauer(), timedelta(hours=5))

    def test_get_pause(self):
        d1 = duty.Duty("1", "09:00:00", "11:00:00")
        d2 = duty.Duty("1", "13:00:00", "16:00:00")
        c1 = duty.Coupe(d1, d2)
        self.assertEqual(c1.getPause(), timedelta(hours=2))

if __name__ == '__main__':
    unittest.main()
