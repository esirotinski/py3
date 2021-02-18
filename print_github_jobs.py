#!/usr/bin/env python3
"""
Details: https://jobs.github.com/api

* This script was not thoroughly tested.
* Remove or edit User-Agent before running.
"""

__author__ = 'Eugene Sirotinski'
__author_email__ = 'sea@gmx.es'
__copyright__ = 'Copyright (c) Eugene Sirotinski'
__license__ = 'MIT'

import json, requests, sys
from termcolor import colored
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError

def printJobs(key: str = '') -> None:
    page = 1
    jobs_total = 0
    url = 'https://jobs.github.com/'

    session = requests.Session()
    adapter = requests.HTTPAdapter(max_retries=2)
    session.mount(url, adapter)

    url += 'positions.json'
    headers = {
        'User-Agent': '<some_string_here> [Contact: example@example.org]'
        }
    while page < 25:
        params = {'page': page, 'search': key}

        try:
            resp = session.get(url, headers = headers, params = params)
            resp.raise_for_status()
        except ConnectionError as e:
            print('Exception occured:', e)
        else:
            print(colored('HTTP ' + str(resp.status_code), 'green'), resp.url)
            data = resp.json()
            if data == []:
                break
            for item in data:
                print(
                    colored("Company: " + item['company'], "yellow"),
                    f"JobTitle: {item['title']}",
                    f"Location: {item['location']}",
                    f"Type: {item['type']}",
                    f"URL: {item['url']}",
                    f"CreatedAt: {item['created_at']}",
                    '', sep = "\n"
                )
                jobs_total += 1
        page += 1
    print("jobs_total:", jobs_total)


if __name__ == "__main__":
    #TODO: argparse. Add args as specified in github doc.
    if len(sys.argv) < 2:
        printJobs()
    else:
        printJobs(sys.argv[1])
