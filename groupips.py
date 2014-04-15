#!/usr/bin/env python3
#
# Copyright 2014 Ryan Peck
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Fast functions for gathering info on a group of IPv4 or IPv6 Networks.

Library contains functions used to learn details and generalize about a list of
IPv4 and IPv6 addresses and networks.

Based almost exclusively on the capbilities of the ipaddress module.

"""


import ipaddress

from collections import defaultdict
from itertools import combinations


__version__ = '0.0.1'


def _group_IPs(ip_objs, bits):
    """ Group IPs by the bits that match """

    super_nets = set([i.supernet(new_prefix=bits) for i in ip_objs])

    group = defaultdict(int)

    while ip_objs != []:
        n = ip_objs.pop()
        for x in super_nets:
            if x.overlaps(n):
                group[str(x)] += 1
                break

    # Return it to a normal dictionary
    return dict(group)


def group_IPv6s(ips, bits):
    ip_objs = [ipaddress.IPv6Network(i) for i in ips]
    return _group_IPs(ip_objs, bits)


def group_IPv4s(ips, bits):
    """ Group IPs by the bits that match """

    ip_objs = [ipaddress.IPv4Network(i) for i in ips]
    return _group_IPs(ip_objs, bits)


def totalAddresses(ips):
    """ Returns the number of total unique addresses in a list of networks """
    ips = listify_params(ips)

    total = 0

    overlapping_bit = False

    # If networks overlap - handle differently
    for a, b in combinations(ips, 2):
        if a.overlaps(b):
            overlapping_bit = True

    if overlapping_bit:
        ips = _overlapping_bits(ips)

    for i in ips:
        total += i.num_addresses

    return total


def _overlapping_bits(ips):
    overlapping_bit = False

    # Networks that contain others.
    master_networks = set()

    two_pair_combinations = combinations(ips, 2)

    for a, b in two_pair_combinations:
        if a.prefixlen == b.prefixlen:
            if a == b:
                master_networks.add(a)
        elif a.prefixlen < b.prefixlen:
            if a.overlaps(b):
                master_networks.add(a)
        else:
            if b.overlaps(a):
                master_networks.add(b)

    # Check if there is any overlap in master_networks
    for a, b in combinations(master_networks, 2):
        if a.overlaps(b):
            overlapping_bit = True

    if overlapping_bit:
        return _overlapping_bits(master_networks)
    else:
        return master_networks


def listify_params(args):
    """
    Create a list of IP Network Objects from parameters, must be either IPv4
    or IPv6...
    """
    assert(validate_ips_param(args))

    ipv4_bool = False
    ipv6_bool = False

    if isinstance(args, str):
        args = [ipaddress.ip_network(args, strict=False)]

    new_args = []

    for i in args:
        n = ipaddress.ip_network(i, strict=False)

        if isinstance(n, ipaddress.IPv4Network):
            ipv4_bool = True
        if isinstance(n, ipaddress.IPv6Network):
            ipv6_bool = True

        # Can't have both types in a list...
        assert(ipv6_bool ^ ipv4_bool)

        new_args.append(n)

    return new_args


# TODO Write tests for this
def validate_ips_param(ips):
    """
    Validate that the parameters passed are types we accept.
    """

    # Acceptable inputs
    assert(isinstance(ips, (str, list, ipaddress.IPv4Network)))

    # Unpack a list
    if isinstance(ips, list):
        for i in ips:
            assert(isinstance(i, (str, ipaddress._BaseNetwork)))

            if isinstance(i, str):
                assert(validate_IPNetwork_str(i))

    return True


# TODO Write tests for this
# Should use ipaddress.ip_network here
def validate_IPNetwork_str(string):
    """ Validate that a valid IP Network string was passed """
    if isinstance(string, str):
        temp = ipaddress.ip_network(string, strict=False)
        del temp

    return True
