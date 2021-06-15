#!/usr/bin/env python3
"""
Prints exchange rates from www.bnm.md
Please update User-Agent and email to suit your details or needs.

"""

__author__ = 'Eugene Sirotinski'
__author_email__ = 'sea@gmx.es'
__copyright__ = 'Copyright (c) Today Eugene Sirotinski'
__license__ = 'MIT'


from datetime import date
from termcolor import colored
from pathlib import Path
import xml.etree.ElementTree as ET
import requests


def get_and_store_xml() -> None:
    today = date.today().strftime('%d.%m.%Y')
    out_file = Path(f'/tmp/official_exchange_rates_{today}.xml')
    uri = 'https://www.bnm.md/ro/official_exchange_rates?get_xml=1&date=' + today
    headers = {'User-Agent':'Example Bot [Contact: bot@example.com]'}

    response = requests.get(uri, headers=headers)

    with out_file.open('wb') as file:
        file.write(response.content)
    parse_xml(out_file)


def parse_xml(file: Path) -> None:
    with file.open('r', encoding='utf-8') as xml:
        xml_tree = ET.parse(xml)
    print_rates(xml_tree)


def print_rates(xml_tree: ET.ElementTree) -> None:
    root = xml_tree.getroot()
    date = 'Date: ' + root.attrib['Date']

    print(colored(date, 'yellow'))
    for i in range(5):
        print(root[i][2].text, root[i][1].text, ' = ', root[i][4].text)


if __name__ == '__main__':
    get_and_store_xml()
