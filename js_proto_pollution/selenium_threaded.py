import concurrent.futures
import sys
import threading
from pathlib import Path
from selenium import webdriver

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

    try:
        browser.get(url)
    except Exception as e:
        print(url, "EXCEPTION occured:", e)
    else:
        current_url = browser.current_url
        if "?" in current_url:
            current_url += "&__proto__[flue]=bart"
        else:
            current_url += "?__proto__[flue]=bart"
        try:
            browser.get(current_url)
        except Exception as e:
            print("CURRENT URL exception:", current_url, e)
        else:
            key = browser.execute_script("return window.flue;")
            if key:
                print("Vulnerable:", current_url, "key = ", key)
            else:
                print("Not vulnerable", current_url, "key = ", key)


def run_requests(urls: list) -> None:
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(print_current_url, urls)


if __name__ == "__main__":
    filename = Path(sys.argv[1])
    with filename.open("r", encoding="utf-8") as file:
        urls = file.readlines()
    urls = [url.strip() for url in urls]

    run_requests(urls)

