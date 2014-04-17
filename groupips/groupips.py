#!/usr/bin/env python3

import collections
import ipaddress


# Add a function that will identify the type of IPs and group them all
# together - like ipaddress functions.


class _BaseGroup:
    """A generic group of IP Addresses/Networks

    This class will containt version indepenent methods for grouping.

    """

    def __init__(self, ip_objs, net_bits, t):
        self.IPVersion = t

        self.addrs = self._listify_params(ip_objs)

        self.net_bits = net_bits

        self.group = self._group_IPs(self.net_bits)

    def _group_IPs(self, bits):
        """ Group IPs by the bits that match """

        self.super_nets = set([i.supernet(new_prefix=bits)
                               for i in self.addrs])

        ip_objs = self.addrs

        group = collections.defaultdict(int)

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

            assert(isinstance(n, self.IPVersion))

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


class IPv4Group(_BaseGroup):
    """Group of IPv4 Addresses"""

    def __init__(self, ip_objs, net_bits=24):
        _BaseGroup.__init__(self, ip_objs, net_bits, ipaddress._BaseV4)


class IPv6Group(_BaseGroup):
    """Group of IPv6 Addresses"""

    def __init__(self, ip_objs, net_bits=48):
        _BaseGroup.__init__(self, ip_objs, net_bits, ipaddress._BaseV6)
