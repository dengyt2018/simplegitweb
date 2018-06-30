#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = 'simplegitweb',
    version = '0.1.3',
    author = 'dengyt',
    author_email = 'dengyt@dengyt.net',
    description = ('A Python git web server that base on dulwich lib'),
    license = 'Apache License, Version 2.0',
    keywords = 'git gitserver gitweb version control',
    packages = find_packages(exclude=['*.git', '*.conf']),
    package_data = {
        'simplegitweb': 'templates/*.html'
        },
    include_package_data=True,
    install_requires=[
        'dulwich>=0.19.0',
        'pathlib>=1.0.0',
        'configparser>=3.5.0',
        'Jinja2>=2.10'
        ],
    zip_safe = False
    )
