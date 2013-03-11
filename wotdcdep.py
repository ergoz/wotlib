# gneposis-wotdcdep 1.0 by Adam Szieberth (2013)

# World of Tanks dossier-cache depickler. Converts dossier-cache
# file to a more portable data file.
# Written in Python 2.7. Well, yes I do programming in hungarian.

# Output format:
# ----------------------------------------------------------------------------
# First line: dossier_cache version.
# Second line: user info if able to fetch it from dossier_cache filename, else
# "?;?".
# Then each tank in the following format (\n stands for newline):
# 1. (key_1, key_2)\n
# 2. timestamp value\n
# 3. raw data of tank until \n(key_1, key_2) of next tank:
#    here each byte represents a value of 0..255.

# If imported, the WoTDossierCache class provides some extra functions for
# making some data more useable. Use help(WoTDossierCache) for more info.

# Derived from Marius Czyz's World of Tanks Dossier Cache to JSON program
# http://github.com/Phalynx/WoT-Dossier-Cache-to-JSON

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
import cPickle
import os
import struct
import sys

JELENTES_KIT = ".data"

class WoTDossierCache(list):
    """Reads a World of Tanks dossier-cache file and provides a list of the
       data."""
    def __init__(self, cache_fajl):

        self.path, fajl = os.path.split(os.path.abspath(cache_fajl))
        self.fajl_nev, self.fajl_kit = os.path.splitext(fajl)

        try:    self.base32nev = base64.b32decode(self.fajl_nev)
        except: self.base32nev = "?;?"

        with open(cache_fajl, "rb") as dc_fajl:
            cache = cPickle.load(dc_fajl)

        self.verzio = cache[0]

        for tank in cache[1].items():
            self.append({
                "key_1"         : tank[0][0],
                "key_2"         : tank[0][1],
                "tank_timestamp": tank[1][0],
                "tank_adat"     : tank[1][1],
                })

    def nemzet_id(self, sor):
        """Returns the nation ID for a tank of given index."""
        return self[sor]["key_2"] >> 4 & 15

    def tank_id(self, sor):
        """Returns the tank ID for a tank of given index."""
        return self[sor]["key_2"] >> 8 & 65535

    def tank_adat(self, sor):
        """Returns tank data of tank of given index."""
        tank_struct = str(len(self[sor]["tank_adat"]))+"B"
        return struct.unpack(tank_struct, self[sor]["tank_adat"])

    def uj_adat(self, ki_fajl):
        """Generates a more portable data of the dossier-cache and writes it
           to file ki_fajl."""
        tartalom = "{}\n{}\n".format(self.verzio, self.base32nev)

        for tank in self:
            tartalom += "({};{})\n{}\n{}\n".format(
                    str(tank["key_1"]),
                    str(tank["key_2"]),
                    tank["tank_timestamp"],
                    tank["tank_adat"]
                )

        with open(ki_fajl, "wb") as out_file:
            out_file.write(tartalom)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "gneposis-wotdcdep 1.0 by Adam Szieberth (2013)"
        print "usage: wotdcdep dossier_cache_file <output_file>"
        print "The output_file gets {} extension by default.".format(
                JELENTES_KIT)
    else:
        dossier_cache = WoTDossierCache(sys.argv[1])

        try:    ki_fajl = sys.argv[2]
        except: ki_fajl = "{}/{}{}".format(
                        dossier_cache.path,
                        dossier_cache.fajl_nev,
                        JELENTES_KIT
                    )

        dossier_cache.uj_adat(ki_fajl)
