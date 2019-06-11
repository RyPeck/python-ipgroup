#!/usr/bin/env python3
#
# Copyright 2019 Ryan Peck
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

from setuptools import setup
from os import path

import ipgroup


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ipgroup",
    maintainer="Ryan Peck",
    maintainer_email="ryan@rypeck.com",
    version=ipgroup.__version__,
    url="https://github.com/RyPeck/python-ipgroup",
    license="Apache License, Version 2.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Telecommunications Industry",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet",
        "Topic :: Internet :: Log Analysis",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Networking",
        "Topic :: Utilities",
    ],
    description="Functions to gather info on a group of IPv4 or IPv6 Networks",
    py_modules=["ipgroup"],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
