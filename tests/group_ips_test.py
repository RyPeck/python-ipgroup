#!/usr/bin/env python3

import ipaddress
import random
import unittest

import groupips.groupips as groupips


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

        group = groupips.group_IPs(IPs, 16)

        self.assertEqual(expected_results, group)

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

        group = groupips.group_IPs(IPs, 24)

        self.assertEqual(expected_results, group)

    def test_group3(self):
        """ 'Random' test """

        # Small Netblock so we don't do over 2**22 hosts to test with
        random_cidr = random.randint(22, 30)

        network = ipaddress.IPv4Network(("129.21.0.0/%s" % random_cidr))

        # So out sample size is never bigger than the population of hosts
        random_int = random.randint(1, 2**(32 - random_cidr - 1))

        IPs = random.sample(set(network.hosts()), random_int)

        expected_results = {("129.21.0.0/%s" % random_cidr): random_int}

        group = groupips.group_IPs(IPs, random_cidr)

        self.assertEqual(expected_results, group)

if __name__ == "__main__":
    unittest.main()
