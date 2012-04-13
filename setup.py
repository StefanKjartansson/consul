#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

NAME = 'consul'

install_requires = [
    'jinja2',
    'requests',
    'six',
]

if sys.version_info < (2, 7):
    install_requires.append('argparse')

setup(
    name = NAME,
    version = "0.1",
    packages = find_packages(),
    install_requires = install_requires,
    author="Stefan Kjartansson",
    author_email="esteban.supreme@gmail.com",
    description="Console Scripts",
    long_description=open('README.md').read(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    entry_points={
        'console_scripts': [
            'appstart = consul.bin.appskeleton:main',
            'grayappend = consul.bin.grayappend:main',
            'makemod = consul.bin.makemodule:main',
        ],
    },
    zip_safe=False,
)
