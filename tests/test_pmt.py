import unittest
from sl2pm.pmt import gain, pmt_output


class TestPMT(unittest.TestCase):
    def test_gain(self):
        self.assertEqual(gain(3), 1)
        self.assertEqual(gain(3.0), 1)
        self.assertEqual(gain(1.0), 3)
        with self.assertRaises(ZeroDivisionError):
            gain(0)

    def test_pmt_output(self):
        self.assertEqual(pmt_output(4, 3), 4.0)
        with self.assertRaises(ZeroDivisionError):
            pmt_output(4, 0)
