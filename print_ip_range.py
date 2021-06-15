#!/usr/bin/env python3
"""
Prints IP addresses in a network range:
$ python3 print_ip_range.py 192.168.0.1/24
$ python3 print_ip_range.py 2001:db00::0/126

For more details: https://docs.python.org/3/library/ipaddress.html
"""

__author__ = 'Eugene Sirotinski'
__author_email__ = 'sea@gmx.es'
__copyright__ = 'Copyright (c) Today Eugene Sirotinski'
__license__ = 'MIT'

import sys
from ipaddress import ip_network, IPv4Address, IPv6Address
from typing import Union, Tuple, Any

Network = Tuple[Union[IPv4Address, IPv6Address], Union[str, int]]

def check_input(argv: Any) -> None:
    if type(argv) is tuple: # ipv6=(42540766411282592856903984951653826560, 126)
        print_address(argv) # ipv4=(23556556, 28)
    elif type(argv) is int: # 32/128-bits int
        print_address(argv)
    elif type(argv) is str: # 32/128-bits int | str IPv4/IPv6 w/|w/o netmask
        if argv.isdigit() and argv.isdecimal():
            print_address(int(argv))
        else:
            print_address(argv)
    else:
        print(f'What was that?\n {type(argv) = }\n {argv = }\n')

def print_address(range: Union[str, int, Network]) -> None:
    try:
        network = ip_network(range, strict=False)
        for address in network.hosts():
            print(address)
    except Exception as e:
        print(e.__class__.__name__, e, sep=': ')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('IPv4/IPv6/integer range/address needed!')
        sys.exit(2)
    else:
        check_input(sys.argv[1])

