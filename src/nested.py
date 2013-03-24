"""
Module for manage nested dictionaries.
Usage: Dict()
"""

# nested.py by Adam Szieberth (2013)
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

class Dict(dict):
    """
    Nested dictionary.

    Usage:
    >>> d = Dict()
    >>> d[('key1', 'key2', 'key3')] = 'val1'
    >>> d
    {'key1': {'key2': {'key3': 'val1'}}}
    >>> d[['key1', 'key22']] = 'val2'
    >>> d
    {'key1': {'key2': {'key3': 'val1'}, 'key22': 'val2'}}
    >>> d[[10,11]] = 12
    >>> d
    {'key1': {'key2': {'key3': 'val1'}, 'key22': 'val2'}, 10: {11: 12}}
    >>> d['a'] = 'b'
    >>> d
    {'key1': {'key2': {'key3': 'val1'}, 'key22': 'val2'}, 10: {11: 12},
        'a': 'b'}
    """
    def __setitem__(self, *args):
        if (len(args) == 2
                    ) and (
                isinstance(args[0], list) or isinstance(args[0], tuple)
                    ) and (
                len(args[0]) >= 1):
            self._setnesteditem(args, self)
        else:
            super().__setitem__(*args)

    def _setnesteditem(self, setitem_args, current_dict):

        class NotDictionary(Exception): pass
        if not isinstance(current_dict, dict):
            raise NotDictionary(
                    'Dictionary was expected, got {}'
                    .format(type(current_dict))
                )

        keys_ = setitem_args[0]
        first_key = keys_[0]
        value = setitem_args[1]
        next_args = keys_[1:], value

        if not current_dict.__contains__(first_key):
            if len(keys_) > 1:
                current_dict[first_key] = dict()
            elif len(keys_) == 1:
                current_dict[first_key] = value

        if len(keys_) > 1:
            return self._setnesteditem(next_args, current_dict[first_key])


if __name__ == '__main__':
    pass