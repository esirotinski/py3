#!/usr/bin/env python3

import concurrent.futures
import sys
import threading
import time
from pathlib import Path

import requests
from requests import exceptions
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError, HTTPError

thread_local = threading.local()


def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def get_header_print_status_code(ip_address):
    ip_address = ip_address.strip()
    URL = "http://" + ip_address + "/"
    HEADERS = {"Connection":"close",
        "User-Agent":"Applicatie scopuri educationale. Contact: sea@gmx.es"}

    session = get_session()
    adapter = HTTPAdapter(max_retries=1)
    session.mount(URL, adapter)

    try:
        response = session.head(URL, headers=HEADERS, timeout=(5, 5), allow_redirects=False)
        # response.raise_for_status()
    except ConnectionError as err:
        print(ip_address, 'CONN ERR:', err)
    except HTTPError as err:
        print(ip_address, 'HTTP ERR:', err)
    except Exception as e:
        print("Exception raised: ", e)
    else:
        print(ip_address, response.status_code, response.headers)


def request_all(ip_addresses):
    with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
        executor.map(get_header_print_status_code, ip_addresses)


if __name__ == "__main__":
    start_time = time.time()

    filename = Path(sys.argv[1])
    with filename.open("r", encoding="utf-8") as file:
        ip_addresses = file.readlines()

    request_all(ip_addresses)
    print(f"Executed in {(time.time() - start_time):.2f} seconds")
