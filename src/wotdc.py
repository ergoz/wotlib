"""
Module for parsing World of Tanks dossier_cache files.
Usage: Get(dossier_cache_file)
"""

# wotdc.py by Adam Szieberth (2013)
# Python 3.3 (Arch Linux)

# Full license text:
# ------------------------------------------------------------------------
#              DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                        Version 2, December 2004

# Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

# Everyone is permitted to copy and distribute verbatim or modified copies
# of this license document, and changing it is allowed as long as the name
# is changed.

#              DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#    TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

# 0. You just DO WHAT THE FUCK YOU WANT TO.
# ------------------------------------------------------------------------
import os
import struct

import depickler
from jsondata import Tanks
import sdf
import tankstats

SDF_DIR = 'data/structs'
SDF_EXTENSION = '.sdf'
# Note: SDF_DIR must contain sdf files named as version integers,
#       e.g. 26.sdf

class Get(dict):
    def __init__(self, dossier_cache_file):
        result = {}
        self.depickled = depickler.WoTDossierCache(dossier_cache_file)

        self.tanks = Tanks()

        sdf_list = [int(f.rstrip(SDF_EXTENSION))
                        for f in os.listdir(SDF_DIR)]
        sdf_defs_list = [sdf.StructDefinition(
                             '{}/{}{}'.format(SDF_DIR, v, SDF_EXTENSION))
                            for v in sdf_list]

        self.structures = dict(zip(sdf_list, sdf_defs_list))


        for tank in self.depickled:
            tank_filt = self.tanks.filt({
                                'countryid': depickler.countryid(tank),
                                'tankid': depickler.tankid(tank),
                            })
            if len(tank_filt) != 1:
                raise Exception

            try:
                tank_name = str(tank_filt[0]['title_short'])
            except:
                tank_name = str(tank_filt[0]['title'])

            tank_timestamp = self.depickled[tank][0]
            tank_data = self.depickled[tank][1]
            tank_data_version = struct.unpack('=h', tank_data[:2])[0]
            tank_struct = self.structures[tank_data_version]
            tank_parseddata = tank_struct.get_dict(tank_data,
                                                   force_length=False)

            result[tank_name] = TankData(tank_parseddata)

        super().__init__(result)

class TankData(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def damage_ratio(self):
        dealt = self['tankdata']['damageDealt']
        received = self['tankdata']['damageReceived']
        result = tankstats.damage_ratio(dealt, received)
        if isinstance(result, float):
            return '{:.2f}'.format(result)
        else:
            return result


if __name__ == '__main__':
    import time

    t1 = time.clock()

    d = Get('data/dossiers/dossier_0840.dat')

    t2 = time.clock()

    x = sorted(d, key=lambda x: d[x].damage_ratio())
    for i in reversed(x):
        print('{}\t{}\t{}'.format(d[i].damage_ratio(),
                                  d[i]['tankdata']['battlesCount'],
                                  i))

    t3 = time.clock()

    print(t2-t1, t3-t2)


    pass