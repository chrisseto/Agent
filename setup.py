#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content


setup(
    name='agent',
    version=__import__('agent').__version__,
    description='Async generators for humans',
    long_description=read('README.md'),
    license=read('LICENSE'),
    author='Chris Seto',
    author_email='chriskseto@gmail.com',
    url='https://github.com/chrisseto/Agent',
    py_modules=['agent'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    test_suite='tests',
)
