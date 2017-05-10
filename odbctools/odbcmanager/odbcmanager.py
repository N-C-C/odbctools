import pypyodbc as odbc
import csv
from configparser import ConfigParser


class OdbcManager:
    def __init__(self):
        config = ConfigParser()
        config.read('config.ini')
        self.connection_name = config.get('odbc', 'DSN')

    def __enter__(self):
        self.__conn = odbc.connect('DSN={0};'.format(self.connection_name))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__conn.close()

    def get_dictionaries(self, query_string, params=None):
        """
        Queries data source
        :param query_string: The query to execute 
        :param params: Parameters to pass to query
        :return: The result of the query as a list of dictionaries
        """
        header, rows = self.query(query_string, params)
        result_list = []
        for row in rows:
            result_list.append(dict(zip(header, row)))
        return result_list

    def write_to_csv(self, file_path, query_string, params=None, delimiter=',', quotechar='"'):
        """
        Queries data source and writes results to file
        :param file_path: Target output path
        :param query_string: The query to execute
        :param params: Parameters to pass to query
        :param delimiter: Character to separate fields in output 
        :param quotechar: Character to quote fields in output
        """
        header, rows = self.query(query_string, params)
        with open(file_path, 'w', newline='') as csv_file:
            wr = csv.writer(csv_file, delimiter=delimiter, quotechar=quotechar, quoting=csv.QUOTE_ALL)
            wr.writerow(header)
            wr.writerows(rows)

    def query(self, query_string, params=None):
        """
        Queries data source
        :param query_string: The query to execute
        :param params: Parameters to pass to query
        :return: A list that contains (0)A list containing the query columns (1) A 
        """
        cur = self.__conn.cursor()
        cur.execute(query_string, params)
        header = [col[0] for col in cur.description]
        rows = []
        for row in cur.fetchall():
            rows.append([col.rstrip(' ') if type(col) is str else col for col in row])
        return [header, rows]