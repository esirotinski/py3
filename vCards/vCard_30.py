#!/usr/bin/env python3
"""
[m8] Autonomous System Number class.
"""

__author__ = 'Eugene Sirotinski'
__author_email__ = 'sea@gmx.es'
__copyright__ = 'Copyright (c) 2020 Eugene Sirotinski'
__license__ = 'MIT'

import sys
import traceback

from AutonomousSystem import AutonomousSystem
from Organisation import Organisation
from Person import Person
from functions import *

class vCard:
    def __init__(self, path: Path):
        self.file_path = path
        self.vCard_data = read_json_file(self.file_path)

        self.vCard_source = self.get_source_value()
        self.vCard_objects = self.get_vCard_objects()

    def get_source_value(self) -> str:
        try:
            source = self.vCard_data['parameters']['sources']['source'][0]['id']
        except Exception as e:
            traceback.print_exc()
            sys.exit(f'Error in file: {self.file_path}')
        else:
            return source

    def get_vCard_objects(self) -> JsonDict:
        try:
            objects = self.vCard_data['objects']
        except Exception as e:
            traceback.print_exc()
            sys.exit(f'Error in file: {self.file_path}')
        else:
            return objects


if __name__ == '__main__':
    #path = Path.home().glob('git/data/ripe/md/*.ripe.AS1547*.json')
    path = Path.home().glob('git/data/ripe/md/*.ripe.*.json')
    temp_list = []
    final_list = []

    for i in path:
        #print(f'Path: {i}')
        vcard = vCard(i)
        member_list = ['organisation', 'person', 'role']
        attributes_list = []
        uuid_list = []
        vcf_list = []
        person_list = []

        for i in range(len(vcard.vCard_objects['object'])):
            attributes_list.append(vcard.vCard_objects['object'][i]['attributes'])
            if attributes_list[i]['attribute'][0]['name'] in member_list:
                uuid_list.append(generate_uuid1())
        
        #print(uuid_list)
        i = 0
        while i  < len(attributes_list):
            if attributes_list[i]['attribute'][0]['name'] == 'aut-num':
                autnum = AutonomousSystem(
                    attributes_list[i]['attribute'],
                    uuid_list,
                    vcard.vCard_objects['object'][0]['link']['href']
                    )
                i += 1
            elif attributes_list[i]['attribute'][0]['name'] == 'organisation':
                organisation = Organisation(
                    attributes_list[i]['attribute'],
                    autnum.get_vCard()
                    )
                values = [x for x in organisation.get_vCard() if x != 'MISSING']
                vcf_list.append(values)
                i += 1
            elif attributes_list[i]['attribute'][0]['name'] == 'person':
                person = Person(attributes_list[i]['attribute'])
                #print(attributes_list[i])
                #UUID = uuid_list.pop()
                #print(person.get_vCard())
                values = [x for x in person.get_vCard() if x != 'MISSING']
                person_list.append(values)
                #print(f'{UUID = }')
                i += 1
            elif attributes_list[i]['attribute'][0]['name'] == 'role':
                #print(attributes_list[i])
                #UUID = uuid_list.pop()
                #print(f'{UUID = }')
                i += 1
            else:
                print('Something unknown here:', attributes_list[i])
                break

        for i in person_list:
            if i[4] not in temp_list:
                temp_list.append(i[4])
                final_list.append(i)

        # Sorting vCards:
        for item in vcf_list:
            if item[3] not in temp_list:
                temp_list.append(item[3])
                final_list.append(item)

    for vcard in final_list:
        print('\n'.join(vcard))

