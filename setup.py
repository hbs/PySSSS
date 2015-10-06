"""A module for doing Shamir Secret Sharing in GF(256) """

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='PySSSS',
    version='1.1.0',
    description='Shamir Secret Sharing in GF(256)',
    url='https://github.com/hbs/PySSSS',
    author='Mathias Herberts, Brandon Matthews',
    author_email='bmatt@luciddg.com',
    license='Apache 2.0',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache License 2.0',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='cryptography secret sharing sss shamir',
    test_suite = "tests",
    packages=['pyssss']
)
