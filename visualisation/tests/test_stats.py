# Run this test from root of dir
# $ cd ait_asl_a1_data_analysis_from_scratch 
# $ python -m unittest visualisation.tests.test_stats

import unittest

from visualisation import stats

class TestConversions(unittest.TestCase):

    def test_predict_value(self):
        self.assertEqual(4.5, stats.predict_value(5, 0.5, 2))

    def test_get_y_intercept(self):
        x_list = [1,2,3,4]
        y_list = [4,6,4,8]

        self.assertEqual(3.0, stats.get_y_intercept(x_list, y_list))

    def test_get_slope(self):
        x_list = [1,2,3,4]
        y_list = [4,6,4,10]

        self.assertEqual(1.6, stats.get_slope(x_list, y_list))

    def test_calculate_least_squares_variables(self):

        x_list = [1,2,3,4]
        y_list = [4,6,4,10]

        self.assertEqual((1.6,2.0), stats.calculate_least_squares_variables(x_list, y_list))

    def test_get_cords_for_best_fit_line(self):
        x_list = [1,2,3,4]
        y_list = [4,6,4,10]
        self.assertEqual(((1, 3.6), (4, 8.4)), stats.get_cords_for_best_fit_line(x_list, y_list))