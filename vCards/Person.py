#!/usr/bin/env python3
"""
[m8] Person class.
"""

__author__ = 'Eugene Sirotinski'
__author_email__ = 'sea@gmx.es'
__copyright__ = 'Copyright (c) 2020 Eugene Sirotinski'
__license__ = 'MIT'

from dataclasses import dataclass
from functions import *
from constants import m8_constants

@dataclass(order=True)
class Person():
    def __init__(self, attributes: JsonDict):
        self.attributes = attributes
        self.get = get_attribute_from(self.attributes)
        self.get_list = get_attribute_list_from(self.attributes)
        self.person = self.get('person')
        self.address = self.get('address')
        self.notify = self.get_list('notify')
        self.email = self.get_list('e-mail')
        self.phone = self.get_list('phone')
        self.fax_no = self.get_list('fax-no')
        self.nic_hdl = self.get('nic-hdl')
        self.created = self.get('created')
        self.source = self.get('source')
        self.link = get_link(attributes)

    def fix_lists(self, string: str, attribute_list: List):
        if attribute_list:
            if string.find('TEL;WORK') != -1:
                return '\n'.join([string + s for s in attribute_list])
            elif string.find('EMAIL') != -1:
                return '\n'.join([string + s for s in attribute_list])
        else:
            return 'MISSING'

    def get_vCard(self):
        return (
            f'BEGIN:VCARD',
            f'VERSION:{m8_constants["vCard_VERSION"]}',
            f'CLASS:private',
            f'N:{self.person.replace(" ",";")}',
            f'FN:{self.person}',
            f'CATEGORIES:Person,{self.source}',
            f'TITLE:{self.link[0]["referenced-type"].upper()}',
            f'URL:{self.link[0]["link"]["href"]}',
            f'NOTE:{self.nic_hdl}',
            f'ADR;work:{self.address}',
            self.fix_lists("TEL;WORK:", self.phone),
            self.fix_lists("TEL;WORK;FAX:", self.fax_no),
            self.fix_lists("EMAIL;WORK:", self.email),
            self.fix_lists("EMAIL;WORK:", self.notify),
            f'BDAY:{self.created}',
            f'END:VCARD'
        )
