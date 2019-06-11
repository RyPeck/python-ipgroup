IP Grouping Python
==================
[![Build
Status](https://travis-ci.org/RyPeck/python-ipgroup.svg?branch=master)](https://travis-ci.org/RyPeck/python-ipgroup) [![Coverage
Status](https://coveralls.io/repos/RyPeck/python-ipgroup/badge.png)](https://coveralls.io/r/RyPeck/python-ipgroup) [![Downloads](https://pypip.in/download/ipgroup/badge.svg)](https://pypi.python.org/pypi/ipgroup/ ) [![License](https://pypip.in/license/ipgroup/badge.svg)](https://pypi.python.org/pypi/ipgroup/) [![Supported Python versions](https://pypip.in/py_versions/ipgroup/badge.svg)](https://pypi.python.org/pypi/ipgroup/) [![Development Status](https://pypip.in/status/ipgroup/badge.svg)](https://pypi.python.org/pypi/ipgroup/)

## Usage

```
>>> import ipgroup
>>> from pprint import pprint
>>> ips = ["129.21.3.17", "129.21.206.5", 
           "8.8.8.8", "8.8.4.4", "192.168.1.1",
           "192.168.255.1", "172.16.5.6", "172.17.20.1"]
>>> example1 = ipgroup.IPv4Group(ips, 16)
>>> pprint(example1.group)
{'129.21.0.0/16': 2,
 '172.16.0.0/16': 1,
 '172.17.0.0/16': 1,
 '192.168.0.0/16': 2,
 '8.8.0.0/16': 2}
>>> example2 = ipgroup.IPv4Group(ips, 12)
>>> pprint(example2.group)
{'129.16.0.0/12': 2, 
 '172.16.0.0/12': 2, 
 '192.160.0.0/12': 2, 
 '8.0.0.0/12': 2}
>>> 
>>> total = ipgroup.totalAddresses(["1.0.0.0/8",
...                                  "1.0.0.0/4",
...                                  "2.0.0.0/8",
...                                  "2.0.0.0/16",
...                                  "2.1.1.0/24",
...                                  "1.0.0.0/16",
>>> total
268435456
```
