#!/usr/bin/env python3
"""
Prints IP addresses in a network range:
$ python3 print_ip_range.py 192.168.0.1/24
$ python3 print_ip_range.py 2001:db00::0/126

If integer provided, will display address only, not a range.
For more details: https://docs.python.org/3/library/ipaddress.html
"""

__author__ = 'Eugene Sirotinski'
__author_email__ = 'sea@gmx.es'
__copyright__ = 'Copyright (c) 2020 Eugene Sirotinski'
__license__ = 'MIT'


import sys, ipaddress
from typing import Union

def check_argument(argv: str) -> None:
    if argv.isdigit():
        print_address(int(argv))        
    else:
        print_address(argv)

def print_address(range: Union[str, int]) -> None:
    try:
        network = ipaddress.ip_network(range, strict=False)
        for address in network.hosts():
            print(address)
    except Exception as e:
        print(e.__class__.__name__, e, sep=': ')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('IPv4/IPv6/integer range/address needed!')
        sys.exit(2)
    else:
        check_argument(sys.argv[1])
