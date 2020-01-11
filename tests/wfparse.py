import unittest
from tektronix import wfparse

ex = "2;16;BIN;RI;MSB;2500;\"Ch1, DC coupling, 2.0E0 V/div, 2.5E-5 s/div, 2500 points, Sample mode\";Y;1.0E-7;0;-1.25E-4;\"s\";3.125E-4;0.0E0;-1.1008E4;\"Volts\""

class CurveTest(unittest.TestCase):
    def test_lex_wfmpre(self):
        result = wfparse.split_string(ex)
        self.assertEqual(result, [
            '2','16', 'BIN', 'RI', 'MSB', '2500',
            'Ch1, DC coupling, 2.0E0 V/div, 2.5E-5 s/div, 2500 points, Sample mode',
            'Y', '1.0E-7', '0', '-1.25E-4', 's', '3.125E-4', '0.0E0', '-1.1008E4', 'Volts'])

        self.assertEqual(wfparse.split_string('"\\""'), ['"'])
        self.assertRaises(wfparse.FormatException, lambda: wfparse.split_string('asd";sad'))
        self.assertRaises(wfparse.FormatException, lambda: wfparse.split_string('asd;"adsad'))

    def test_parse_wfmpre(self):
        result = wfparse.WfmPresets.parse(ex)


if __name__ == '__main__':
    unittest.main()