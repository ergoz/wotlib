"""
Module for parsiing binary data by an SDF (struct definition) file.
Usage: StructDefinition(sdf_file)
"""

# sdf.py by Adam Szieberth (2013)
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
import struct

import nested

FORMAT_DEF_CHARS = '@=<>!'

class StructDefinition(list):
    """
    Parses binary data with an SDF file.
    Usage: StructDefinition(sdf_file)

    SDF file format:
      - At very first is the format definition character (@=<>!)
        followed by a newline. For more info:
        http://docs.python.org/3.3/library/struct.html#format-characters

      - The list does not contain this character, but you can get it:
        >>> StructDefinition(sdf_file).type_

      - The rest of the lines have a format character (e.g. 'b' or 'i')
        followed by a tab followed by a the name of the data it
        represents. The name can be delimited with '/'s to define
        subcategories if necessary.

      - For example ('N|' for line number, '...' for missing parts):

          1|=
          2|b   tankdata/version
          3|l	 tankdata/creationTime
             ...
         25|h	 series/sniperSeries
             ...

        Here first line declares native byte order with standard size. The
        second line represents a signed char (integer) of one byte in
        size, and declares that it contains version of tankdata.

      - A line can also contain definition of pad bytes (e.g. bytes which
        are unnecessary). This declaration stands alone in the line:

         26|6x

        Here we declared a six bytes long garbage.
    """
    class SDFSyntaxError(Exception): pass
    class InvalidFormatDefinitionChar(Exception): pass

    def __init__(self, sdf_file):
        with open(sdf_file) as _sdf_file:
            sdf_raw_data = _sdf_file.read().splitlines()

            if sdf_raw_data[0] not in [char for char in FORMAT_DEF_CHARS]:
                raise self.InvalidFormatDefinitionChar(
                        'Invalid format definition character: {}'
                        .format(sdf_raw_data[0])
                    )

            self.type_ = sdf_raw_data[0]
            sdf_raw_data = sdf_raw_data[1:]

            for e in enumerate(sdf_raw_data):
                row_data = tuple(e[1].split('\t'))

                if len(row_data) > 2:
                    raise self.SDFSyntaxError(
                        'SyntaxError in SDF row: {}!'.format(row))

                sdf_raw_data[e[0]] = row_data

            super().__init__(sdf_raw_data)

    def format(self):
        """Returns the struct format string."""
        result = self.type_
        for elem in self:
            result += elem[0]
        return result

    def size(self):
        """Returns the size of binary data which can be parsed."""
        return struct.calcsize(self.format())

    def reduced(self):
        """
        Trims the pad byte definition parts of the declaration list and
        returns the trimmed list. Since struct.unpack returns a list of
        values in order but excludes pad byte parts this is useful to
        match its result with the list of names.
        """
        result = []
        for i in enumerate(self):
            if len(i[1]) == 2:
                result.append(i[1])
        return result

    def parse(self, data, force_length=True):
        """
        Parses a binary data and returns a list of tuples of name, value
        pairs. Here name denotes full name string, e.g. for line 2 in
        example of main class docstring: ('tankdata/version', 26)

        Longer data is also accepted if force_length keyword argument is
        False. This case parsing starts from start of data and ends where
        it ends.
        """
        class WrongDataLength(Exception): pass

        if force_length and len(data) != self.size():
            raise WrongDataLength(
                    'Data length of {} expected, got {}'
                    .format(self.size(), len(data))
                )

        elif not force_length and len(data) < self.size():
            raise WrongDataLength(
                    'Data length of minimum {} expected, got {}'
                    .format(self.size(), len(data))
                )

        if not force_length:
            data = data[:self.size()]

        data_array = struct.unpack(self.format(), data)
        reduced_self = self.reduced()


        if len(data_array) != len(reduced_self):
            raise Exception

        result = list()
        for e in enumerate(data_array):
            result.append((reduced_self[e[0]][1], e[1]))

        return result

    def get_dict(self, data, force_length=True):
        """
        Parses a binary data and returns a dictionary. The dictionary
        becomes nested if the SDF line name contained '/', e.g. for line 2
        in example of main class docstring:

        >>> s = StructDefinition(sdf_file)
        >>> s.get_dict(data)['tankdata']['version']
        >>> 26

        force_length works exactly the same as for parse().
        """
        result = nested.Dict()
        for i in self.parse(data, force_length=force_length):
            result[i[0].split('/')] = i[1]
        return result

if __name__ == '__main__':
    pass