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

Dependencies
------------
* pypyodbc

Licence
--------
MIT

