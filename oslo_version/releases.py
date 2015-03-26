# -*- coding: utf-8 -*-

#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import enum


class Releases(enum.Enum):
    """Known openstack releases.

    See: http://en.wikipedia.org/wiki/OpenStack#Release_history
    """

    AUSTIN = 'A'
    BEXAR = 'B'
    CACTUS = 'C'
    DIABLO = 'D'
    ESSEX = 'E'
    FOLSOM = 'F'
    GRIZZLY = 'G'
    HAVANA = 'H'
    ICEHOUSE = 'I'
    JUNO = 'J'
    KILO = 'K'
    LIBERTY = 'L'

    # Taken from python enum docs...
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


def match(text):
    """Case insensitive match a string to its enumeration.

    If no match is found then none is returned.
    """
    text_lower = text.lower()
    for e in list(Releases):
        if e.name.lower() == text_lower:
            return e
        if e.value.lower() == text_lower:
            return e
    return None


# Expose the above enumerations at the module level...
AUSTIN = Releases.AUSTIN
BEXAR = Releases.BEXAR
CACTUS = Releases.CACTUS
DIABLO = Releases.DIABLO
ESSEX = Releases.ESSEX
FOLSOM = Releases.FOLSOM
GRIZZLY = Releases.GRIZZLY
HAVANA = Releases.HAVANA
ICEHOUSE = Releases.ICEHOUSE
JUNO = Releases.JUNO
KILO = Releases.KILO
LIBERTY = Releases.LIBERTY
