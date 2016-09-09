#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
]

test_requirements = [
]

setup(
    name='SRL',
    version='0.1.0',
    description="Python implementation of SRL.",
    long_description=readme + '\n\n' + history,
    author="Simple Regex Language",
    maintainer='Lin Ju',
    maintainer_email='soasme@gmail.com',
    platforms='any',
    url='https://github.com/SimpleRegex/SRL-Python',
    packages=find_packages(exclude=('tests', 'tests.*', '*.tests', '*.tests.*', )),
    package_dir={'srl': 'srl'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='re,regex,srl,simpleregex',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Text Processing',
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
