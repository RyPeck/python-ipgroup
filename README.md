IP Grouping Python
==================
[![Build
Status](https://travis-ci.org/RyPeck/IP-Grouping-Python.png?branch=master)](https://travis-ci.org/RyPeck/IP-Grouping-Python) [![Coverage Status](https://coveralls.io/repos/RyPeck/IP-Grouping-Python/badge.png)](https://coveralls.io/r/RyPeck/IP-Grouping-Python)

## Usage

Script requires Python 3.3, which is the first version of Python to include the [ipaddress manipulation library](http://docs.python.org/3.3/library/ipaddress) in the standard release.

~~~
>>> import groupips
>>> from pprint import pprint
>>> ips = ["129.21.3.17", "129.21.206.5", 
           "8.8.8.8", "8.8.4.4", "192.168.1.1",
           "192.168.255.1", "172.16.5.6", "172.17.20.1"]
>>> 
>>> pprint(groupips.group_IPs(ips, 16))
{'129.21.0.0/16': 2,
 '172.16.0.0/16': 1,
 '172.17.0.0/16': 1,
 '192.168.0.0/16': 2,
 '8.8.0.0/16': 2}
>>> pprint(groupips.group_IPs(ips, 12))
{'129.16.0.0/12': 2, 
 '172.16.0.0/12': 2, 
 '192.160.0.0/12': 2, 
 '8.0.0.0/12': 2}
~~~

## Next Features to Do

- IPv6 Support
- Read in from CSV File
- Error Catching based on Input
- Experiment with different return features
    - Return `ipaddress` Network objects.
