#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [] # Intentionally left empty, despite ghdiff needed for some certain features.

# see requirements_*.txt for lists of relevant test/doc/maintenance dependencies.
test_requirements = [] #TODO, read in all lists of requirements files.

version = '0.3.0'

setup(
    name='pyenvdiff',
    version=version,
    description="Python environment comparison tool.",
    long_description=readme + '\n\n' + history,
    author="Jeffrey McLarty",
    author_email='jeffrey.mclarty@gmail.com',
    url='https://github.com/jnmclarty/pyenvdiff-lib',
    download_url='https://github.com/jnmclarty/pyenvdiff-lib/tarball/' + version,
    packages=[
        'pyenvdiff',
    ],
    package_dir={'pyenvdiff': 'pyenvdiff'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD license",
    zip_safe=False,
    keywords='pyenvdiff',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent'
    ],
    test_suite='tests',
    tests_require=test_requirements
)
