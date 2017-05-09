import unittest
from odbctools import OdbcManager


class OdbcManagerTest(unittest.TestCase):
    # Mock csv to make sure file gets written.
    def test_query_to_csv(self):
        with OdbcManager() as cars:
            cars.write_to_csv("..\\test-out\\res.csv", "select * from id_rec where id=?", [976811])

    def test_get_dictionary_trimmed(self):
        with OdbcManager() as cars:
            result_set = cars.get_dictionaries("select * from id_rec where id=?", [976811])
            andrew = result_set[0]
            self.assertEqual(andrew['lastname'], "Yatsko")
