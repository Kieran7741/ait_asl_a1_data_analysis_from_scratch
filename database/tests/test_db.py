# Run this test from root of dir
# $ cd ait_asl_a1_data_analysis_from_scratch 
# $ python -m unittest database.tests.test_db

import unittest

from database.db import DB, create_dict_from_db_query


class TestDb(unittest.TestCase):

    def setUp(self) -> None:
        self.db = DB('../players.db')

    def test_create_dict_from_db_query(self):

        result = create_dict_from_db_query([('David De Gea Quintana', '€205K'),
                                            ('Paul Pogba', '€250K')],
                                           ['Name', 'Wage'])

        self.assertEqual(result, {'Name': ['David De Gea Quintana', 'Paul Pogba'],
                                  'Wage': ['€205K', '€250K']})

    def test_create_db_object_fails_if_not_file_exists(self):

        self.assertRaises(EnvironmentError, DB, 'no/such/database.db')

    def test_select__simple_select(self):

        result = self.db.select(['Name'])

        self.assertEqual(len(result['Name']), 18547)
        self.assertTrue('Lionel Messi' in result['Name'])

    def test_select__non_dict_return_type(self):
        result = self.db.select(['Name'], where='Club="Manchester United"', dict_result=False)
        self.assertTrue(isinstance(result, list))

    def test_select__with_where(self):

        result = self.db.select(['Name'], where='Club="Manchester United"')

        self.assertEqual(len(result['Name']), 33)
        self.assertTrue('Paul Pogba' in result['Name'])

    def test_validate_team__team_in_dataset(self):

        self.assertTrue(self.db.validate_team('Liverpool'))

    def test_validate_team__team_not_in_dataset(self):

        self.assertFalse(self.db.validate_team('ASL FC'))


if __name__ == '__main__':
    unittest.main()
