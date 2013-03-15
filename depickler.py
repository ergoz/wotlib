"""
Module for depickling World of Tanks dossier_cache files.
Usage: WoTDossierCache(dossier_cache_file)
"""

# depickler.py by Adam Szieberth (2013)
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

import base64
import os
import pickle

ENCODING = 'latin_1'
# valid encodings: cp1256, latin_1, iso8859_9

DOSSIER_KEY_0 = 2
# no other key used


def countryid(dossier_key):
    """Returns the countryid from dossier_key."""
    return dossier_key[1] >> 4 & 15

def tankid(dossier_key):
    """Returns the tankid from dossier_key."""
    return dossier_key[1] >> 8 & 65535

def key(countryid, tankid):
    """Returns key used in dossier cache."""
    return (tankid << 8)+(countryid << 4)+1

def dossier_key(countryid, tankid):
    """Returns dossier cache key."""
    return DOSSIER_KEY_0, key(countryid, tankid)


def _base32namepart(name, i):
    """Returns name.split(';')[i] if not '?', None otherwise."""
    result = name.split(';')[i]
    if result != '?':
        return result


class WoTDossierCache(dict):
    """
    Dictionary for storing World of Tanks dossier_cache data:

    Keys are tuples of two integers (I named the tuple as dossier_key):
        - first integer is always 2
        - second integer is a binary mix of 1, countryid, and tankid:
          (tankid << 8) + (countryid << 4) + 1
    Values are two item lists:
        - first item is the timestamp integer
        - second item is binary data of the achievements with tank

    The WoTDossierCache dictionary have the following attributes:
        - version: returns the integer of dossier_cache version
        - base32name: returns the server;username string fetched from the
          filename of the dossier_cache_file; if file was renamed it returns
          ?;?.
    """
    def __init__(self, cache_file):

        self.path, file_ = os.path.split(os.path.abspath(cache_file))
        self.file_name, self.file_ext = os.path.splitext(file_)

        try:
            self.base32name = base64.b32decode(self.file_name)
        except:
            self.base32name = "?;?"
        else:
            self.base32name = self.base32name.decode(ENCODING)

        with open(cache_file, mode='rb') as dc_file:
            cache = pickle.load(dc_file, encoding=ENCODING)

        self.version = cache[0]
        super().__init__(cache[1])

    def wotserver(self):
        """
        Returns the address of World of Tanks server from base32name;
        returns None if unknown.
        """
        return _base32namepart(self.base32name, 0)

    def nick(self):
        """
        Returns the nickname from base32name; returns None if unknown.
        """
        return _base32namepart(self.base32name, 1)


if __name__ == '__main__':
    pass
