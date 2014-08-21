#!/usr/bin/env python3

import ipaddress
import random
import unittest

import ipgroup


class TestGroupIPs(unittest.TestCase):
    def setUp(self):
        pass

    def test_group(self):
        IPs = ["127.0.0.1",
               "127.0.1.1",
               "127.1.1.1",
               "127.1.0.1",
               "127.2.0.1",
               "127.2.1.1",
               ]

        expected_results = {"127.0.0.0/16": 2,
                            "127.1.0.0/16": 2,
                            "127.2.0.0/16": 2,
                            }

        a = ipgroup.IPv4Group(IPs, 16)

        self.assertEqual(expected_results, a.group)

    def test_group2(self):
        IPs = ["127.0.0.1",
               "127.0.1.1",
               "127.1.1.1",
               "127.1.0.1",
               "127.2.0.1",
               "127.2.1.1",
               ]

        expected_results = {"127.0.0.0/24": 1,
                            "127.0.1.0/24": 1,
                            "127.1.0.0/24": 1,
                            "127.1.1.0/24": 1,
                            "127.2.0.0/24": 1,
                            "127.2.1.0/24": 1,
                            }

        b = ipgroup.IPv4Group(IPs, 24)

        self.assertEqual(expected_results, b.group)

    def test_group3(self):
        """ 'Random' test """

        # Small Netblock so we don't do over 2**10 hosts to test with
        random_cidr = random.randint(22, 30)

        network = ipaddress.IPv4Network(("129.21.0.0/%s" % random_cidr))

        # So out sample size is never bigger than the population of hosts
        random_int = random.randint(1, 2**(32 - random_cidr - 1))

        IPs = random.sample(set(network.hosts()), random_int)

        expected_results = {("129.21.0.0/%s" % random_cidr): random_int}

        c = ipgroup.IPv4Group(IPs, random_cidr)

        self.assertEqual(expected_results, c.group)

    def test_IPv6(self):
        """ 'Random' test """

        # Small Netblock so we don't do over 2**10 hosts to test with
        random_cidr = random.randint(118, 126)

        network = ipaddress.IPv6Network(("2607:f8b0:4009:803::/%s" %
                                        random_cidr))

        # So out sample size is never bigger than the population of hosts
        random_int = random.randint(1, 2**(128 - random_cidr - 1))

        IPs = random.sample(set(network.hosts()), random_int)

        expected_results = {("2607:f8b0:4009:803::/%s" % random_cidr):
                            random_int}

        d = ipgroup.IPv6Group(IPs, random_cidr)

        self.assertEqual(expected_results, d.group)

    def test_reGroup(self):
        IPs = ["127.0.0.1",
               "127.1.0.1",
               "127.1.1.1",
               ]

        expected_results1 = {"127.0.0.0/24": 1,
                             "127.1.0.0/24": 1,
                             "127.1.1.0/24": 1,
                             }

        g = ipgroup.IPv4Group(IPs, 24)

        self.assertEqual(expected_results1, g.group)

        expected_results2 = {"127.0.0.0/16": 1,
                             "127.1.0.0/16": 2,
                             }

        g.reGroup(16)

        self.assertEqual(expected_results2, g.group)


class TestTotalAddresses(unittest.TestCase):
    """
    Tests totalAddresses function returns correct number of unique addresses
    in various scenarios
    """

    def setUp(self):
        pass

    def test_total_address1(self):
        self.assertEqual(8, ipgroup.totalAddresses("127.0.0.0/29"))

    def test_total_address2(self):
        total = ipgroup.totalAddresses(["192.168.1.1/16",
                                         "127.0.0.0/16",
                                         ])

        self.assertEqual(2**17, total)

    def test_total_address3(self):
        total = ipgroup.totalAddresses(["192.168.1.1/16",
                                         "127.0.0.0/28"
                                         ])

        self.assertEqual((2**16 + 2**4), total)

    def test_total_address4(self):
        total = ipgroup.totalAddresses(["128.151.2.0/24",
                                         "128.151.2.0/30",
                                         ])

        self.assertEqual(2**8, total)

    def test_total_address5(self):
        total = ipgroup.totalAddresses(["128.151.2.0/24",
                                         "128.151.2.0/23",
                                         ])

        self.assertEqual(2**9, total)

    def test_total_address_overlapping(self):
        """ For the scenario where networks will contain eachother. """
        total = ipgroup.totalAddresses(["129.21.0.0/16",
                                         "129.21.1.0/18",
                                         "129.21.1.0/24",
                                         ])

        self.assertEqual(2**16, total)

    def test_total_address_overlapping2(self):
        """ For the scenario where networks will contain eachother big networks
        to show that the function is fast, no longer enumerating all networks.
        """
        total = ipgroup.totalAddresses(["1.0.0.0/8",
                                         "2.0.0.0/8",
                                         "2.0.0.0/16",
                                         "2.1.1.0/24",
                                         "1.0.0.0/16",
                                         "1.1.1.0/24",
                                         "2.0.0.0/8",
                                         ])

        self.assertEqual((2**24 + 2**24), total)

    def test_total_address_overlapping3(self):
        """ For the scenario where networks will contain eachother big networks
        to show that the function is fast, no longer enumerating all networks.
        """
        total = ipgroup.totalAddresses(["1.0.0.0/8",
                                         "1.0.0.0/4",
                                         "2.0.0.0/8",
                                         "2.0.0.0/16",
                                         "2.1.1.0/24",
                                         "1.0.0.0/16",
                                         "1.1.1.0/24",
                                         "2.0.0.0/8",
                                         ])

        self.assertEqual(2**28, total)

    def test_total_address_overlap_IPv6(self):
        total = ipgroup.totalAddresses(['2620:008d:8000::/48',
                                         '2620:008d:8000:e693::/64',
                                         ])

        self.assertEqual(2**80, total)


if __name__ == "__main__":
    unittest.main()
