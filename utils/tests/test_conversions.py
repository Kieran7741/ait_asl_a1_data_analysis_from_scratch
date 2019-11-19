# Run this test from root of dir
# $ cd ait_asl_a1_data_analysis_from_scratch 
# $ python -m unittest utils.tests.test_conversions

import unittest
from unittest.mock import Mock, patch

from utils import conversions

class TestConversions(unittest.TestCase):

    def test_convert_money_string__k_prefix(self):
    
        self.assertEqual(200.0*1000, conversions.convert_money_string('$200k'))
    
    def test_convert_money_string__m_prefix(self):

        self.assertEqual(200.0*1000000, conversions.convert_money_string('$200m'))

    def test_convert_money_string__invalid_value_passed(self):

        self.assertEqual(0, conversions.convert_money_string('not a number'))

    def test_convert_feet_to_cm__correct_string_format(self):

        self.assertEqual(182.88, conversions.convert_feet_to_cm("6'0"))
        self.assertEqual(167.1, conversions.convert_feet_to_cm("5'6"))
    
    def test_convert_feet_to_cm__invalid_string_returns_zero(self):
        self.assertEqual(0, conversions.convert_feet_to_cm('invalid height'))

    def test_convert_weight_lbs_to_kg__correct_string_format(self):

        self.assertEqual(68.04, conversions.convert_weight_lbs_to_kg('150lbs'))
        
    def test_convert_feet_to_cm__invalid_string_returns_zero(self):
        self.assertEqual(0, conversions.convert_feet_to_cm('invalid weight'))
