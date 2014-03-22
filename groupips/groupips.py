#!/usr/bin/env python3

import collections
import ipaddress


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
