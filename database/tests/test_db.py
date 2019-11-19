# Run this test from root of dir
# $ cd ait_asl_a1_data_analysis_from_scratch 
# $ python -m unittest database.tests.test_db

import unittest

from database import db

class TestDb(unittest.TestCase):

    def test_create_db(self):
        dab = db.DB('database/players.db')