# Copyright Mark Jenkins, 2013
#
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved. This file is offered as-is,
# without any warranty.
# http://www.gnu.org/prep/maintain/html_node/License-Notices-for-Other-Files.html
# @author Mark Jenkins <mark@markjenkins.ca>

from math import log

from .encoding import (
    create_reverse_dictionary, sym_decode
    )

DICTIONARY = tuple( str(i) for i in range(1, 6+1) )
REVERSE_DICTIONARY = create_reverse_dictionary(DICTIONARY)

def dice_decode(v):
    dice_buffer = tuple(v)
    length = int( (log(6, 2) * len(dice_buffer)) // 8 )+1
    return sym_decode(dice_buffer, REVERSE_DICTIONARY, length)
