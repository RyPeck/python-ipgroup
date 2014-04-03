#!/usr/bin/env python3

import collections
import ipaddress

from itertools import combinations


def _group_IPs(ip_objs, bits):
    """ Group IPs by the bits that match """

    super_nets = set([i.supernet(new_prefix=bits) for i in ip_objs])

    group = collections.defaultdict(int)

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
    ips = listify_params(ips)

    total = 0

    overlapping_bit = False

    # Need to check if any of the networks overlap, and use a different method
    # for getting the number of unique addresses
    for a, b in combinations(ips, 2):
        if a.overlaps(b):
            overlapping_bit = True

    if overlapping_bit:
        super_set = set()
        for i in ips:
            s = set(list(i.hosts()))
            super_set = super_set.union(s)

        # Return all address... + 2 for non-usable hosts
        return len(super_set) + 2

    for i in ips:
        total += i.num_addresses

    return total


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
