from collections import deque

import pypyodbc as odbc
import csv
from configparser import ConfigParser


class OdbcManager:
    def __init__(self, auto_commit=False, dsn='', connection_string='', config_file='config.ini', config_section='odbc', config_key='DSN'):
        self.connection_name = None
        if dsn:
            self.connection_name = 'DSN={0}'.format(dsn)
        elif connection_string:
            self.connection_name = connection_string
        else:
            self.connection_name = self.__get_dsn_config(config_file, config_key, config_section)

        if not self.connection_name:
            raise ConnectionError("Must specify DSN via ini file or in the dsn parameter.")

        self.__conn = odbc.Connection
        self.auto_commit = auto_commit

    def __get_dsn_config(self, config_file, config_key, config_section):
        config = ConfigParser()
        config.read(config_file)
        return config.get(config_section, config_key)

    def __enter__(self):
        self.open_connection()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

    def open_connection(self):
        """
        Opens ODBC connection
        """
        if self.connection_name:
            self.__conn = odbc.connect(self.connection_name, self.auto_commit)

    def close_connection(self):
        """
        Closes ODBC connection
        """
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

    def get_dictionaries_in_queue(self, query_string, params=None):
        """
        Queries data source, returns a queue (for appending speed)
        :param query_string: The query to execute
        :param params: Parameters to pass to query
        :return: The result of the query as a deque of dictionaries
        """
        header, rows = self.query(query_string, params)
        results = deque()
        for row in rows:
            results.append(dict(zip(header, row)))
        return results

    def write_to_csv(self, file_path, query_string, params=None, delimiter=',', quotechar='"', quoting=True, escapechar=None, csv_quoting=None, column_names= None):
        """
        Queries data source and writes results to file :param file_path: Target output path :param query_string: The
        query to execute :param params: Parameters to pass to query :param delimiter: Character to separate fields in
        output :param quotechar: Character to quote fields in output :param quoting: True to quote False for no
        quoting :param escapechar: if quoting is set to QUOTE_NONE and escapechar is not set, the writer will raise
        :param column_names: list of column names to override the default from the query.
        :param csv_quoting: csv package constants, override quoting if specified.
        Error if any characters that require escaping are encountered. Per docs.python.org documentation for CSV.
        """
        header, rows = self.query(query_string, params)
        if not column_names:
            column_names = header

        quoting = csv.QUOTE_ALL if quoting else csv.QUOTE_NONE
        quoting = csv_quoting if csv_quoting is not None else quoting
        with open(file_path, 'w', newline='') as csv_file:
            wr = csv.writer(csv_file, delimiter=delimiter, quotechar=quotechar, quoting=quoting, escapechar=escapechar)
            wr.writerow(column_names)
            wr.writerows(rows)

    def query(self, query_string, params=None):
        """
        Queries data source
        :param query_string: The query to execute
        :param params: Parameters to pass to query
        :return: A list that contains (0)A list containing the query columns (1) A list of the resulting data (rows)
        """
        cur = self.__conn.cursor()
        cur.execute(query_string, params)
        header = [col[0] for col in cur.description]
        rows = []
        for row in cur.fetchall():
            rows.append([col.rstrip(' ') if type(col) is str else col for col in row])
        return [header, rows]

    def query_no_resultset(self, query_string, params=None, commit=None):
        """
        For running DDL/DML queries for creating, deleting, updating database objects.
        :param query_string: The query to execute
        :param params: Parameters to pass to query
        :param commit: If option is used, does not update database, but still use caution
        :return: Message indicating transaction was committed\n
                True = Was committed\n
                False = Not committed
        """
        cur = self.__conn.cursor()
        cur.execute(query_string, params)

        if commit is None:
            if self.auto_commit:
                cur.commit()
                return True
        if commit:
            cur.commit()
            return True
        return False

