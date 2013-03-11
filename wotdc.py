# gneposis-wotdc 1.0 by Adam Szieberth (2013)

# Converts World of Tanks dossier-cache to plain text data.
# Written in Python 2.7. Well, yes I do programming in hungarian.

# Output format:
# ----------------------------------------------------------------------------
# First line: dossier_cache version.
# Second line: user info if able to fetch it from dossier_cache filename, else
# "?;?".
# Then one line per tank in the following format:
# unknown_id;nation_id;tank_id;timestamp;raw_data.
# Here raw_data is a representation of hexadecimal values formatted to take
# two characters of space e.g. 0 -> 00, 255 -> FF.

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
    def __init__(self, cache_fajl):

        self.path, fajl = os.path.split(os.path.abspath(cache_fajl))
        self.fajl_nev, self.fajl_kit = os.path.splitext(fajl)

        try:    self.base32nev = base64.b32decode(self.fajl_nev)
        except: self.base32nev = "?;?"

        with open(cache_fajl, "rb") as dc_fajl:
            cache = cPickle.load(dc_fajl)

        self.verzio = cache[0]

        for tank in cache[1].items():
            tank_struct = str(len(tank[1][1]))+"B"
            tank_adat   = struct.unpack(tank_struct, tank[1][1])
            self.append({
                "ismeretlen_id" : tank[0][0],
                "nemzet_id"     : tank[0][1] >> 4 & 15,
                "tank_id"       : tank[0][1] >> 8 & 65535,
                "tank_timestamp": tank[1][0],
                "tank_adat"     : tank_adat,
                })

    def jelentes(self, output_fajl):
        tartalom = "{}\n{}\n".format(self.verzio, self.base32nev)

        for tank in self:
            tartalom += "{};{};{};{};".format(
                    str(tank["ismeretlen_id"]),
                    str(tank["nemzet_id"]),
                    str(tank["tank_id"]),
                    tank["tank_timestamp"]
                )

            for elem in tank["tank_adat"]:
                tartalom += "%0.2X" % elem
            tartalom += "\n"

        with open(output_fajl, "w") as out_file:
            out_file.write(tartalom)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "gneposis-wotdc 1.0 by Adam Szieberth (2013)"
        print "usage: wotdc dossier_cache_file <output_file>"
        print "The output_file gets {} extension by default.".format(
                JELENTES_KIT)
    else:
        dossier_cache = WoTDossierCache(sys.argv[1])

        try:    output_fajl = sys.argv[2]
        except: output_fajl = "{}/{}{}".format(
                        dossier_cache.path,
                        dossier_cache.fajl_nev,
                        JELENTES_KIT
                    )

        dossier_cache.jelentes(output_fajl)
