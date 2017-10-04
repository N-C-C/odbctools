import unittest


from odbctools import OdbcManager


class OdbcManagerTest(unittest.TestCase):
    # Mock csv to make sure file gets written.
    # def test_query_to_csv(self):
    #     query_string = ""
    #     params = []
    #     with OdbcManager() as ds:
    #         ds.write_to_csv("..\\test-out\\res.csv", query_string, [])
    #
    # def test_get_dictionary_trimmed(self):
    #     query_string = ""
    #     params = []
    #     with OdbcManager() as ds:
    #         result_set = ds.get_dictionaries(query_string, params)
    #         first_result = result_set[0]

    def test_get_dictionaries_in_queue(self):
        query_string = "select first 100000 * from id_rec"
        params = []
        with OdbcManager() as ds:
            result_set = ds.get_dictionaries_in_queue(query_string, params)
            self.assertEqual(len(result_set), 100000)

    def test_get_dictionaries(self):
        query_string = "select first 100000 * from id_rec"
        params = []
        with OdbcManager() as ds:
            result_set = ds.get_dictionaries(query_string, params)
            self.assertEqual(len(result_set), 100000)

    def test_encapsulated_connection(self):
        class Foo:
            def __init__(self):
                self.connection = OdbcManager(dsn='unity64')

            def __enter__(self):
                self.connection.open_connection()
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.connection.close_connection()

        with Foo() as f:
            data = f.connection.get_dictionaries('select top 1 * from people', list())
        print(data)
