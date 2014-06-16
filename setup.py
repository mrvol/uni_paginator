# -*- coding: utf-8 -*-
from setuptools import find_packages
from distutils.core import setup

__author__ = 'mrvol'

setup(
    name='uni_paginator',
    version='0.1.0',
    author='Vladimir Ageykin',
    author_email='mrvol777@gmail.com',
    packages=['uni_paginator'],  # find_packages(), #['uni_paginator',],
    package_data={'uni_paginator': ['templates/**',]},
    # scripts=,
    url='https://github.com/mrvol/uni_paginator',
    license='BSD',
    description='Universal django paginator for data (QuerySet, List and Sphix Search)',
    long_description=open('README.md').read(),
    include_package_data=True,
    install_requires=[
        "Django >= 1.3.0",
    ],
)