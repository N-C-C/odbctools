from setuptools import setup

setup(
    name='odbctools',
    version='0.1.0',
    packages=['odbctools', 'odbctools.odbcmanager', 'odbctools.tests'],
    install_requires=['pypyodbc'],
    url='https://github.com/N-C-C/odbctools',
    license='',
    author='Andrew Yatsko',
    author_email='ayatsko@live.com',
    description='A set of tools to simplify connecting to and working with an ODBC data source'
)
