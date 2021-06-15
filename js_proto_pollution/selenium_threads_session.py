import concurrent.futures
import threading
from selenium import webdriver
from pathlib import Path
import sys
import time


thread_local = threading.local()

def get_driver():
    if not hasattr(thread_local, "driver"):
        options = webdriver.chrome.options.Options()
        options.headless = False

        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(60)

        thread_local.driver = driver
    return thread_local.driver


def print_current_url(url: str) -> None:
    browser = get_driver()
    browser.get(url)
    print(url, browser.current_url)


def run_requests(urls: list) -> None:
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(print_current_url, urls)


if __name__ == "__main__":
    filename = Path(sys.argv[1])
    with filename.open("r", encoding="utf-8") as file:
        urls = file.readlines()

    urls = [url.strip() for url in urls]
    run_requests(urls)

