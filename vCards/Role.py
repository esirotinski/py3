#!/usr/bin/env python3
"""
[m8] Role class.
"""

__author__ = 'Eugene Sirotinski'
__author_email__ = 'sea@gmx.es'
__copyright__ = 'Copyright (c) 2020 Eugene Sirotinski'
__license__ = 'MIT'

from dataclasses import dataclass
from CommonAttributes import CommonAttributes

@dataclass(frozen=True, order=True)
class Role(CommonAttributes):
    remarks: str
    abuse_mailbox: str
