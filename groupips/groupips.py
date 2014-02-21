#!/usr/bin/env python3

import collections
import ipaddress


def group_IPs(ips, bits):
    """ Group IPs by the bits that match """

    ip_objs = [ipaddress.IPv4Network(i) for i in ips]

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
