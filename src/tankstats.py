"""
Module for common World of Tanks related efficiency stats functions.
"""

# tankstats.py by Adam Szieberth (2013)
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

def damage_ratio(dealt, received):
    if received == 0:
        return float(0)
    return dealt / received