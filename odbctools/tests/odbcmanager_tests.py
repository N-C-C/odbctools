import unittest
from odbctools import OdbcManager


class OdbcManagerTest(unittest.TestCase):
    # Mock csv to make sure file gets written.
    def test_query_to_csv(self):
        query_string = ""
        params = []
        with OdbcManager() as ds:
            ds.write_to_csv("..\\test-out\\res.csv", query_string, [])

    def test_get_dictionary_trimmed(self):
        query_string = ""
        params = []
        with OdbcManager() as ds:
            result_set = ds.get_dictionaries(query_string, params)
            first_result = result_set[0]
