#!/usr/bin/env python3
"""
Prints nameservers by country code.
Nameservers from https://public-dns.info/#countries .

Please edit User-Agent/Contact details before running.

This script was not thoroughly tested.
"""

__author__ = 'Eugene Sirotinski'
__author_email__ = 'sea@gmx.es'
__copyright__ = 'Copyright (c) 2020 Eugene Sirotinski'
__license__ = 'MIT'

import json, requests, sys
from typing import Dict, List

JsonList = List[Dict]

def request_json(country_code: str) -> JsonList:
    data = []
    uri = f'https://public-dns.info/nameserver/{country_code}.json'
    headers = {
        'User-Agent' : '<some_string_here> [Contact: example@example.org]'
        }
    try:
        response = requests.get(uri, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(e.__class__.__name__, e, sep=': ')
    else:
        data = response.json()
    return data

def print_nameservers(data: JsonList) -> None:
    if data == []:
        sys.exit(f'parse_json {data = }')

    for elem in data:
        ns = elem['ip']
        as_org = elem['as_org']
        as_nr = elem['as_number']
        country_id = elem['country_id']
        print(f'nameserver {ns}', ' ' * (22 - len(ns)),
                f'#{country_id} AS{as_nr} {as_org}')


if __name__ == '__main__':
    #TODO: parse args add -6
    if len(sys.argv) < 2:
        print('Please edit User-Agent/Contact details before running.')
        print('Country code missing.')
        print('Available codes: https://public-dns.info/#countries')
        sys.exit(2)
    else:
        data = request_json(sys.argv[1])
        if data:
            print_nameservers(data)
        else:
            print(f'main_json {data = }')
