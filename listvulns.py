#!/usr/bin/env python3
"""
This scripts check if there are any security vulnerable packages on
Debian Linux operating system. It grabs a list of packages from
https://security-tracker.debian.org/tracker/status/release/ + release_name ,
then it checks if any vulnerable package is currently installed.


Another tool which probably does it better (did not try it yet):
https://manpages.debian.org/testing/debsecan/debsecan.1.en.html

Enjoy!
"""

__author__ = 'Eugene Sirotinski'
__author_email__ = 'esirotinski@gmail.com'
__copyright__ = 'Copyright (c) Eugene Sirotinski'
__license__ = 'MIT'

import platform
import re
import subprocess
import sys
from typing import List

from selenium import webdriver
from selenium.webdriver.common.by import By


URL = 'https://security-tracker.debian.org/tracker'


def return_os_release() -> str:
    release = subprocess.getoutput('lsb_release -r')
    # pattern = re.compile(r'(?P<Release>[\w\s]+):\s+(?P<value>\w+)')
    pattern = re.compile(r'([\w\s]+):\s+(\w+)')
    match = pattern.match(release)
    return match.group(2)


def return_installed_packages() -> List:
    # TODO: Add regexp
    # TODO: Add dict key=pkg vers=value
    installed_packages = subprocess.getoutput(
        "apt list --installed 2>/dev/null |grep -v Listing|cut -d\  -f1| \
            sed 's/\/testing,now//g'")
    return installed_packages.split('\n')


def extract_vuln_pkgs_list(release: str) -> List:
    vulnerable_packages_list = []

    options = webdriver.chrome.options.Options()
    options.headless = True
    browser = webdriver.Chrome(options=options)
    print('Requesting ' + URL + '/status/release/' + release + \
        ' to grab vulnerable packages.')
    browser.get(URL + '/status/release/' + release)

    elements_size = len(browser.find_elements(By.XPATH, '//table/tbody/tr'))

    for i in range(1, elements_size):
        xpath = '//table/tbody/tr[' + str(i) + ']/td[1]/a'
        elements = browser.find_elements(By.XPATH, xpath)
        for e in elements:
            if e.text:
                vulnerable_packages_list.append(e.text)
    return vulnerable_packages_list


def print_vulnerable_installed_packages(
    installed_packages_list: List, vulnerable_packages_list) -> None:
    for package in installed_packages_list:
        if package in vulnerable_packages_list:
            print(package, 'is vulnerable! Details: ' + \
                URL + '/source-package/' \
                    + package)


def main() -> None:
    if platform.system() == 'Linux':
        print('Checking if running on a Debian ...')
        if platform.version().__contains__('Debian'):
            installed_packages_list = return_installed_packages()

            os_release = return_os_release()
            print('You are on Debian', os_release + '!')

            vulnerable_packages_list = extract_vuln_pkgs_list(os_release)
            print_vulnerable_installed_packages(
                installed_packages_list, vulnerable_packages_list)
        else:
            print('Currently works on Debian Linux only. Exiting.')
            sys.exit(0)
    else:
        print('Curently works on Linux only. Exiting.')
        sys.exit(0)


if __name__ == '__main__':
    main()

