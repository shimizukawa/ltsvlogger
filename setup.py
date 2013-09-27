# -*- coding: utf-8 -*-
from __future__ import with_statement

from setuptools import setup, find_packages
import os

from ltsvlogger import __version__


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
description = 'labeled TSV logger.'

setup(
    name='ltsvlogger',
    version=__version__,
    description=description,
    long_description=README,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: System :: Logging",
        "Topic :: Utilities",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
    ],
    author="Takayuki SHIMIZUKAWA",
    author_email="shimizukawa@gmail.com",
    url="https://bitbucket.org/shimizukawa/ltsvlogger",
    namespace_packages=[],
    packages=find_packages(),
    py_modules=['ltsvlogger'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    extras_require={},
    entry_points="",
)
