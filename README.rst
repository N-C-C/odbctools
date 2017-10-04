odbctools
=========

Overview
--------
odbc tools is a set of tools to simplify connecting to and working with an ODBC data source. It includes a context manager for handling connections to the data source and the ability to return a result set in an easy to use format or write the results to a file.

Install It
----------
From PyPI ::

    $ pip install odbctools


Use It
------
Odbctools by default uses a file called config.ini, or you can override this for different scenarios, including passing the dsn directly.

Create config.ini ::

    [odbc]
    DSN=SourceName

Code Example ::

    from odbctools import OdbcManager

    query_string = "Your query here"
    params = [p1, p2]

    with OdbcManager() as datasource:
        result_list = datasource.get_dictionaries(query_string, params)
        for result_dict in result_list:
            for col_name, col_data in result_dict.items():
                print("{0}{1}".format(str(col_name).ljust(25), col_data))

Another Example ::

    from odbctools import OdbcManager

    query_string = "Your query here"
    params = [p1, p2]

    with OdbcManager(dsn='ODBC Name Here') as datasource:
        result_list = datasource.get_dictionaries_in_queue(query_string, params)
        for result_dict in result_list:
            for col_name, col_data in result_dict.items():
                print("{0}{1}".format(str(col_name).ljust(25), col_data))

Encapsulating the connection in your classes is also possible ::

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

Returning data from a query
---------------------------
**query** - Returns list that contains [0]A list containing the query columns [1:] A list of the resulting data (rows)

**get_dictionaries** - Queries data source, returns a list of dictionaries.

**get_dictionaries_in_queue** - Queries data source, returns a deque of dictionaries.

**write_to_csv** - Queries data source and writes results to a CSV file

Updating data
-------------
*Note: by default commit is turned off, if you want to enable auto commit, you can set it when creating the OdbcManager object or when calling this function.*

**query_no_resultset** - For running DDL/DML queries for creating, deleting, updating records.


Dependencies
------------
* pypyodbc

License
--------
MIT

