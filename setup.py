from setuptools import setup


def readme():
    with open('README.rst') as file:
        return file.read()


setup(
    name='odbctools',
    version='0.7.0',
    license='MIT',
    author='Andrew Yatsko',
    author_email='ayatsko@live.com',
    packages=[
        'odbctools',
        'odbctools.odbcmanager',
        'odbctools.tests'
    ],
    url='https://github.com/N-C-C/odbctools',
    description='A set of tools to simplify connecting to and working with an ODBC data source',
    long_description=readme(),
    include_package_data=True,
    keywords='odbc database data sql informix',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Topic :: Database',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],
)
