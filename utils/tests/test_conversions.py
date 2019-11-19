# Run this test from root of dir
# $ cd ait_asl_a1_data_analysis_from_scratch 
# $ python -m unittest utils.tests.test_conversions

import unittest

from utils import conversions

class TestConversions(unittest.TestCase):

    def test_convert_money_string__k_prefix(self):
    
        self.assertEqual(200.0*1000, conversions.convert_money_string('$200k'))
    
    def test_convert_money_string__m_prefix(self):

        self.assertEqual(200.0*1000000, conversions.convert_money_string('$200m'))

    def test_convert_money_string__invalid_value_passed(self):

        self.assertEqual(0, conversions.convert_money_string('not a number'))