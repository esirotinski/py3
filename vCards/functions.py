#!/usr/bin/env python3
"""
[m8] Helper functions here!
"""

__author__ = 'Eugene Sirotinski'
__author_email__ = 'sea@gmx.es'
__copyright__ = 'Copyright (c) 2020 Eugene Sirotinski'
__license__ = 'MIT'

import json
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Union
from uuid import UUID, uuid1

JsonDict = Dict[str, Any]

def generate_uuid1() -> UUID:
    return uuid1()

#TODO: Add 'att_list' type
def get_attribute_list_from(att_list) -> Callable[[Any], List[str]]:
    return lambda value: [
        item['value'] for item in att_list
                        if item['name'] == value]

#TODO: Add 'att_list' type
def get_attribute_from(att_list) -> Callable[[Any], str]:
    return lambda value: ' '.join([
        item['value'] for item in att_list
                        if item['name'] == value])
                        
#TODO: Add 'att_list' type
def get_link(att_list) -> List:
    return [item for item in att_list if len(item) > 2]

def read_json_file(path: Path) -> JsonDict:
    with path.open('r', encoding='utf-8') as file:
        return json.load(file)

def return_json_objects(json_data: JsonDict):
    return json_data['objects']['object']
    
def return_json_objects_length(json_data: JsonDict) -> int:
    return len(json_data['objects']['object'])

def yield_attributes(json_data: JsonDict, key: str) -> Iterable:
    size = len(objects := json_data['objects']['object'])
    for i in range(size):
        if objects[i]['type'] == key:
            for elem in objects[i]['attributes']['attribute']:
                yield elem

def return_object(json_data: JsonDict, key: str) -> List[Any]:
    size = len(objects := json_data['object'])
    obj = []
    for i in range(size):
        if objects[i]['type'] == key:
            obj =  objects[i]
    return obj
