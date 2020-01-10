import unittest
from tektronix import curve
import os.path

script_dir = os.path.dirname(os.path.abspath(__file__))

class CurveTest(unittest.TestCase):
    def test_parse_curve(self):
        with open(os.path.join(script_dir, 'channel-1.bin'), 'rb') as f:
            data = f.read()
        data = curve.parse_curve(data)
        self.assertEqual(len(data), 2500)
        self.assertEqual(data[0], -10496)

if __name__ == '__main__':
    unittest.main()