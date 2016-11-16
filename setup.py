#! /usr/bin/env python
from setuptools import setup

descr = '''Parser for Web of Science (WoS) XML Dataset'''

if __name__ == "__main__":
    setup(
        name='wos_parser',
        version='0.1.dev',
        description='Python parser for Web of Science (WoS) XML Dataset',
        long_description=open('README.md').read(),
        url='https://github.com/titipata/wos_parser',
        author='Titipat Achakulvisut',
        author_email='titipata@u.northwestern.edu',
        license='(c) 2015 Titipat Achakulvisut, Daniel E. Acuna',
        install_requires=['lxml'],
        packages=['wos_parser'],
    )
