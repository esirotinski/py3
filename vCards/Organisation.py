#!/usr/bin/env python3
"""
[m8] Organisation class.
"""

__author__ = 'Eugene Sirotinski'
__author_email__ = 'sea@gmx.es'
__copyright__ = 'Copyright (c) 2020 Eugene Sirotinski'
__license__ = 'MIT'

from dataclasses import dataclass

from AutonomousSystem import AutonomousSystem
from constants import m8_constants
from functions import *


@dataclass(order=True)
class Organisation(AutonomousSystem):
    def __init__(self, attributes: JsonDict, autnum_details: List):
        self.attributes = attributes
        self.get = get_attribute_from(self.attributes)
        self.get_list = get_attribute_list_from(self.attributes)
        self.organisation = self.get('organisation')
        self.org_name = self.get('org-name')
        self.org_type = self.get('org-type')
        self.address = self.get('address')
        self.email = self.get_list('e-mail')
        self.notify = self.get_list('notify')
        self.phone = self.get_list('phone')
        self.fax_no = self.get_list('fax-no')
        self.created = self.get('created')
        self.last_modified = self.get('last-modified')
        self.link = 'URL_HERE' #NOTE: TBU if needed.
        self.geoloc = self.get('geoloc')
        self.language = self.get_list('language')
        self.source = self.get('source')
        self.autnum_details = autnum_details

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
            f'N:{self.org_name.replace(" ",";")}',
            f'FN:{self.org_name}',
            f'{self.autnum_details[3]}',
            f'{self.autnum_details[7]}',
            f'NOTE:{self.autnum_details[6][4:]}',
            f'ADR;work:{self.address}',
            self.fix_lists("TEL;WORK:", self.phone),
            self.fix_lists("TEL;WORK;FAX:", self.fax_no),
            self.fix_lists("EMAIL;WORK:", self.email),
            self.fix_lists("EMAIL;WORK:", self.notify),
            f'{self.autnum_details[7]}',
            f'BDAY:{self.created}',
            #f'{self.autnum_details}',
            f'END:VCARD'
        )

        #f'URL:{self.link}',
        #f'{self.autnum_details[8]}',
        #f'NOTE:lang={self.language}',
        #f'GEO:{self.geoloc.replace(" ", ";")}',
        #f'URL:{self.link}',
        #f'ORG:{self.autnum_details[6][6:]}',
        #f'UID:{self.uuid}',
