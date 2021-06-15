#!/usr/bin/env python3
"""
Read a list of URLs from file and check if vulnerable for
JS prototype pollution.
Example of input file is available: domains.txt
"""

import concurrent.futures
from selenium import webdriver
from pathlib import Path
import sys
import time


def run_request(url: str) -> None:

    options = webdriver.chrome.options.Options()
    options.headless = False

    browser = webdriver.Chrome(options=options)
    browser.set_page_load_timeout(60)

    try:
        browser.get(url)
    except Exception as e:
        print("Exception occured: ", e)
    else:
        current_url = browser.current_url
        if "?" in current_url:
            try:
                url = current_url + "&__proto__[flue]=bart"
                print(f"Checking {url}")
                browser.get(url)
            except Exception as e:
                print("Exception &: ", e)
            else:
                key = browser.execute_script("return window.flue;")
                if key:
                    print(f"VULNERABLE: {key = } {url}")
        else:
            try:
                url = current_url + "?__proto__[flue]=bart"
                print(f"Checking {url}")
                browser.get(url)
            except Exception as e:
                print("Exception ?: ", e)
            else:
                key = browser.execute_script("return window.flue;")
                if key:
                    print(f"VULNERABLE: {key = } {url}")
    finally:
        browser.close()


def run_requests(urls):
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(run_request, urls)


if __name__ == "__main__":
    start_time = time.time()

    filename = Path(sys.argv[1])
    with filename.open("r", encoding="utf-8") as file:
        urls = file.readlines()
    urls = [url.strip() for url in urls]

    run_requests(urls)
    print("Finished in: ", time.time() - start_time)
