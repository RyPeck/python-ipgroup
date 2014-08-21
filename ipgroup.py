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


__version__ = '0.0.2'


class _BaseGroup:
    """A generic group of IP Addresses/Networks

    This class will containt version indepenent methods for grouping.

    """

    def __init__(self, ip_objs, net_bits=None, t=None, cache=True):
        self.IPVersion = t

        self.addrs = self._listify_params(ip_objs)

        if cache:
            self.addrs_cache = self.addrs.copy()

        self.net_bits = net_bits

        if net_bits:
            self.group = self._group_IPs(self.net_bits)

    def reGroup(self, bits):
        """Regroup the IP addresses according to a new CIDR Prefix"""

        self.old_group = self.group
        self.addrs = self.addrs_cache

        new_group = self._group_IPs(bits)

        self.group = dict(new_group)

    def _group_IPs(self, bits):
        """ Group IPs by the bits that match """

        self.super_nets = set([i.supernet(new_prefix=bits)
                               for i in self.addrs])

        ip_objs = self.addrs

        group = defaultdict(int)

        while ip_objs != []:
            n = ip_objs.pop()
            for x in self.super_nets:
                if x.overlaps(n):
                    group[str(x)] += 1
                    break

        # Return it to a normal dictionary
        return dict(group)

    def _listify_params(self, args):
        """
        Create a list of IP Network Objects from parameters, must be either
        IPv4 or IPv6...
        """

        assert(self._validate_ips_param(args))

        if isinstance(args, str):
            args = [ipaddress.ip_network(args, strict=False)]

        new_args = []

        for i in args:
            n = ipaddress.ip_network(i, strict=False)

            # If the IP Type is unset, use whatever comes along first
            if self.IPVersion is not None:
                assert(isinstance(n, self.IPVersion))
            else:
                self.IPVersion == type(n)

            new_args.append(n)

        return new_args

    # TODO Write tests for this
    def _validate_ips_param(self, ips):
        """
        Validate that the parameters passed are types we accept.
        """

        # Acceptable inputs
        assert(isinstance(ips, (str, list, self.IPVersion)))

        # Unpack a list
        if isinstance(ips, list):
            for i in ips:
                assert(isinstance(i, (str, ipaddress._IPAddressBase)))

                if isinstance(i, str):
                    assert(self._validate_IPNetwork_str(i))

        return True

    # TODO Write tests for this
    # Should use ipaddress.ip_network here
    def _validate_IPNetwork_str(self, string):
        """ Validate that a valid IP Network string was passed """

        if isinstance(string, str):
            temp = ipaddress.ip_network(string, strict=False)
            del temp

        return True

    def _overlapping_bits(self, ips):
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
            return self._overlapping_bits(master_networks)
        else:
            return master_networks

    def totalAddresses(self, ip_objs):
        """ Returns the number of total unique addresses in a list of
        networks """
        ips = self._listify_params(ip_objs)

        total = 0

        overlapping_bit = False

        # If networks overlap - handle differently
        for a, b in combinations(ips, 2):
            if a.overlaps(b):
                overlapping_bit = True

        if overlapping_bit:
            ips = self._overlapping_bits(ips)

        for i in ips:
            total += i.num_addresses

        return total


class IPv4Group(_BaseGroup):
    """Group of IPv4 Addresses"""

    def __init__(self, ip_objs, net_bits=24):
        _BaseGroup.__init__(self, ip_objs, net_bits, ipaddress._BaseV4)


class IPv6Group(_BaseGroup):
    """Group of IPv6 Addresses"""

    def __init__(self, ip_objs, net_bits=48):
        _BaseGroup.__init__(self, ip_objs, net_bits, ipaddress._BaseV6)


def totalAddresses(ips):
    """ function for getting total addresses """
    i = _BaseGroup(ips)

    return i.totalAddresses(ips)
