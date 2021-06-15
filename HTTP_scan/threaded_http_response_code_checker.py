#!/usr/bin/env python3
"""
Reads IP addresses from file (one IP per line).
Sends HTTP request port 80 and returns HTTP response code.
"""

import sys
from pathlib import Path
from threading import Thread

import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError, HTTPError


class RunRequests(Thread):
    def __init__(self, IP_addr):
        super().__init__()
        self.IP_addr = IP_addr

    def run(self):
        URL = 'http://' + self.IP_addr + '/'
        HEADERS = {"User-Agent":
            "Applicatie scopuri educationale. Contact: sea@gmx.es"}

        session = requests.Session()
        adapter = HTTPAdapter(max_retries=2)
        session.mount(URL, adapter)

        try:
            response = session.head(URL, headers=HEADERS, timeout=(5, 5), allow_redirects=False)
            response.raise_for_status()
        except ConnectionError as err:
            print(self.IP_addr, 'CONN ERR:', err)
        except HTTPError as err:
            print(self.IP_addr, 'HTTP ERR:', err)
        else:
            print(self.IP_addr, response.status_code, response.headers)


def read_file_and_perform_requests(filename):
    with filename.open('r', encoding='utf-8') as file:
        IP_addresses = file.readlines()

    NUMBER_OF_THREADS = 4

    while IP_addresses:
        for _ in range(NUMBER_OF_THREADS):
            try:
                IP_addr = IP_addresses.pop(0).strip()
            except IndexError:
                break
            else:
                thread = RunRequests(IP_addr)
                thread.start()

        for _ in range(NUMBER_OF_THREADS):
            thread.join()


if __name__ == '__main__':
    read_file_and_perform_requests(Path(sys.argv[1]))

