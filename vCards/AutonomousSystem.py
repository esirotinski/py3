#!/usr/bin/env python3
"""
[m8] Autonomous System class.
"""

__author__ = 'Eugene Sirotinski'
__author_email__ = 'sea@gmx.es'
__copyright__ = 'Copyright (c) 2020 Eugene Sirotinski'
__license__ = 'MIT'

from dataclasses import dataclass

from constants import m8_constants
from functions import JsonDict, List, get_attribute_from


@dataclass(order=True)
class AutonomousSystem:
    def __init__(self, attributes: JsonDict, members_list: List, link: str):
        self.attributes = attributes
        self.get = get_attribute_from(self.attributes)
        self.aut_num = self.get('aut-num')
        self.as_name = self.get('as-name')
        self.link = link
        self.status = self.get('status')
        self.descr = self.get('descr')
        self.source = self.get('source')
        self.created = self.get('created')
        self.default = self.get('default')
        self.members = members_list

    def get_members(self) -> List:
        members = [f'MEMBER:urn:uuid:{val}' for val in self.members]
        return members

    def get_vCard(self) -> List:
        return [
            f'BEGIN:VCARD',
            f'VERSION:{m8_constants["vCard_VERSION"]}',
            f'CLASS:private',
            f'CATEGORIES:{self.source},AS',
            f'N:{self.as_name};{self.aut_num}',
            f'FN:{self.as_name} {self.aut_num}',
            f'ORG:{self.descr}',
            f'TITLE:{self.as_name}',
            f'URL:{self.link}',
            f'BDAY:{self.created}',
            f'END:VCARD'
        ]
 