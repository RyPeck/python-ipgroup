#!/usr/bin/env python3
#
# Copyright 2014 Ryan Peck
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from distutils.core import setup

import ipgroup


setup(
    name='ipgroup',
    maintainer='Ryan Peck',
    maintainer_email='ryan@rypeck.com',
    version=ipgroup.__version__,
    url='https://github.com/RyPeck/IP-Grouping-Python',
    license='Apache License, Version 2.0',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Networking',
        ],
    description='Functions gathering info on a group of IPv4 or IPv6 Networks',
    py_modules=['ipgroup'],
)
