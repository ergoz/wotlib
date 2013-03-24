import glob
import struct

import jsondata

STRUCT_FORMATS = (None, 'b', 'h', None, 'l')

SDF_EXT = '.sdf'

struct_glob_asterisk_at = jsondata.STRUCTURES_GLOB.find('*')
struct_file_left = jsondata.STRUCTURES_GLOB[:struct_glob_asterisk_at]
struct_file_right = jsondata.STRUCTURES_GLOB[struct_glob_asterisk_at:]

def struct_file_version(struct_file):
    return int(struct_file.lstrip(struct_file_left)
                          .rstrip(struct_file_right))


if __name__ == '__main__':
    for struct_file in glob.glob(jsondata.STRUCTURES_GLOB):
        version = struct_file_version(struct_file)
        structures = jsondata.Structures(json_glob=struct_file)
        structures.sort(key=lambda x: x['offset'])

        struct_dat = '=\n'

        for e in enumerate(structures):
            offset = e[1]['offset']
            length = e[1]['length']

            if e[0] == 0 and offset > 0:
                if offset != 2:
                    raise Exception
                struct_dat += 'h\ttankdata/version\n'

            if e[0] < len(structures)-1:
                next_offset = structures[e[0]+1]['offset']
                gap = next_offset - offset - length
                if gap < 0:
                    raise Exception
                else:
                    struct_dat += '{}\t{}/{}\n'.format(
                                                STRUCT_FORMATS[length],
                                                e[1]['category'],
                                                e[1]['name'],
                                            )
                if gap > 0:
                    struct_dat += '{}x\n'.format(gap)

            else:
                struct_dat += '{}\t{}/{}\n'.format(
                                                STRUCT_FORMATS[length],
                                                e[1]['category'],
                                                e[1]['name'],
                                            )

        struct_dat = struct_dat.rstrip('\n')

        with open('{}{}'.format(version, SDF_EXT), mode='w') as dat_file:
            dat_file.write(struct_dat)