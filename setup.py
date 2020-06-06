#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


#if sys.argv[-1] == 'publish':
#    os.system('python setup.py sdist upload')
#    sys.exit()


packages = [
     'marie47esp32',
     'marie47esp32/webserver',
     'marie47esp32/util',
]

package_data = {
}

requires = [
        'click',
        'jsonrpclib-pelix',
]

classifiers = [
        'Development Status :: 1 - Beta',
]

entry_points={
    'console_scripts': [
        'marie47esp32server=marie47esp32:main',
    ],
}

setup(
    name='marie47esp32',
    version="0.0.1",
    description='python server to connect webfrontend with esp32 client',
    long_description="",
    packages=packages,
    package_data=package_data,
    install_requires=requires,
    author="fs, tr",
    author_email='streicher@tentable.de',
    url='http://tentable.de',
    license='MIT',
    classifiers=classifiers,
    python_requires='>=3',
    entry_points=entry_points,
)
