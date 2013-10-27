# Copyright Mark Jenkins, 2013
#
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved. This file is offered as-is,
# without any warranty.
# http://www.gnu.org/prep/maintain/html_node/License-Notices-for-Other-Files.html
# @author Mark Jenkins <mark@markjenkins.ca>

from .encoding import (
    create_reverse_dictionary, sym_decode_with_zero_pad,
    sym_encode_with_zero_pad,
    )

DICTIONARY = tuple(
    '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz' )
REVERSE_DICTIONARY = create_reverse_dictionary(DICTIONARY)

def b58decode(v, length=None):
    return sym_decode_with_zero_pad(v, REVERSE_DICTIONARY)

def b58encode(v):
    return ''.join(sym_encode_with_zero_pad(v, DICTIONARY))

