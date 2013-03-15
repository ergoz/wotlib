"""
Module for handling data stored in plain World of Tanks related JSON files.
Usage: Tanks()
       Maps()
       Structures()

You can even filter the data e.g.:
    Tanks().filt({'country': 'UK', 'tanktype': 'TD', 'tier': 3})
    Structures().filt({'version': 22})
"""

# jsondata.py by Adam Szieberth (2013)
# Python 3.3 (Windows)

# Full license text:
# ----------------------------------------------------------------------------
#                 DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                           Version 2, December 2004
#
# Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
#
# Everyone is permitted to copy and distribute verbatim or modified  copies of
# this license document, and changing it is allowed as long as the name is
# changed.
#
#                 DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#       TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
# 0. You just DO WHAT THE FUCK YOU WANT TO.
# ----------------------------------------------------------------------------

import glob
import re

import depickler

JSON_RE_SAMPLE = '"(?P<key>\w+?)":(?P<value>.+?)[,}]'

MAPS_GLOB = 'maps.json'
STRUCTURES_GLOB = 'structures_*.json'
TANKS_GLOB = 'tanks.json'

COUNTRY = 'country.lst'
TYPE = 'type.lst'


def elem_of_lst(i, list_file):
    """
    Returns an element of list_file.
    list_file should have one element per line and nothing else.
    """
    with open(list_file) as l_file:
        elements = l_file.read().splitlines()
    return elements[i]

def get_uppercased(string):
    """Returns str of uppercased alphabets from string."""
    result = ''
    for ch in string:
        if ch.isalpha() and ch == ch.upper():
            result += ch
    return result


class Structure(dict):
    """Dictionary of structure data."""
    def __init__(self, init_dict={}):
        super().__init__(init_dict)

class Map(dict):
    """Dictionary of map data."""
    def __init__(self, init_dict={}):
        super().__init__(init_dict)

class Tank(dict):
    """Dictionary of tank data."""
    def __init__(self, init_dict={}):
        super().__init__(init_dict)

    def key(self):
        """Returns key used in dossier cache."""
        return depickler.key(self['countryid'], self['tankid'])

    def dossier_key(self):
        """Returns dossier cache key."""
        return depickler.dossier_key(self['countryid'], self['tankid'])

    def country(self):
        """Returns name of the country."""
        return elem_of_lst(self['countryid'], COUNTRY)

    def tanktype(self, longname=False):
        """
        Returns abbreviated type of tank.
        If keyword arg longname=True then it returns the full type string.
        """
        elem = elem_of_lst(self['type'], TYPE)
        if longname:
            return elem
        return get_uppercased(elem)


class DictList(list):
    """Parent class for list which contains dictionaries."""
    class AttrClassIsNotDictError(AttributeError): pass
    class WrongAttrTypeError(AttributeError): pass

    def __init__(self, dictclass, json_glob=None):
        if not issubclass(dictclass, dict):
            raise self.AttrClassIsNotDictError(
                    'Unsupported dictclass (not dict): {}'
                    .format(dictclass)
                )
        self.dictclass = dictclass
        super().__init__([])
        if json_glob:
            for f in glob.glob(json_glob):
                self.append_from_json(f)

    def append(self, item):
        if not isinstance(item, self.dictclass):
            raise self.WrongAttrTypeError(
                    'Unsupported type (not {}): {}'
                    .format(self.dictclass, type(item))
                )
        super().append(item)

    def append_from_json(self, json_file):

        def clean(raw_data):
            '''Cleans a raw JSON data.'''
            raw_data = raw_data.strip()
            raw_data = raw_data.strip('"')

            try:
                return int(raw_data)
            except: pass

            try:
                return float(raw_data)
            except: pass

            return raw_data

        with open(json_file) as json_f:
            json_raw = json_f.readlines()

        line_data = []
        for li in json_raw[1:-2]:
            li_keys = []
            li_vals = []
            li_finditer = re.finditer(JSON_RE_SAMPLE, li)
            for i in li_finditer:
                li_keys.append(i.group('key'))
                li_vals.append(clean(i.group('value')))
            self.append(self.dictclass(zip(li_keys, li_vals)))

    def filt(self, filt_dict):
        """
        Filters tanks by a dictonary.
        Even supports filtering by unique attributes, e.g. for Tank:
        {'country': 'UK', 'tanktype': 'TD'}
        """
        result = DictList(self.dictclass)
        result.__class__ = self.__class__

        magic_attrs = set([attr for attr in dir(self.dictclass)
                       if attr.startswith('__') and attr.endswith('__')
            ])
        unique_attrs = set(dir(self.dictclass)) - magic_attrs - set(dir(dict))

        for item in self:
            match = True
            for key in filt_dict:
                if key in unique_attrs:
                    val = getattr(item, key)()
                else:
                    val = item.get(key)

                if val == filt_dict[key]:
                    match = match and True
                else:
                    match = False

            if match:
                result.append(item)
        return result

class DictListFromJson(DictList):
    """
    List of dictionaries generated by JSON file(s).
    Usage: DictListFromJson('*.json')
           DictListFromJson('tanks.json', Tank)
    Returns an empty list for DictListFromJson(None)
    """
    def __init__(self, json_glob, dictclass=dict):
        super().__init__(dictclass)
        if json_glob is not None:
            for f in glob.glob(json_glob):
                self.append_from_json(f)

class Maps(DictListFromJson):
    """List of Maps."""
    def __init__(self, json_glob=MAPS_GLOB, dictclass=Map):
        super().__init__(json_glob, dictclass)

class Structures(DictListFromJson):
    """List of Structures."""
    def __init__(self, json_glob=STRUCTURES_GLOB, dictclass=Structure):
        super().__init__(json_glob, dictclass)

class Tanks(DictListFromJson):
    """List of Tanks."""
    def __init__(self, json_glob=TANKS_GLOB, dictclass=Tank):
        super().__init__(json_glob, dictclass)


if __name__ == '__main__':
    pass
