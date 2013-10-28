# Copyright Mark Jenkins, 2013
#
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved. This file is offered as-is,
# without any warranty.
# http://www.gnu.org/prep/maintain/html_node/License-Notices-for-Other-Files.html
# @author Mark Jenkins <mark@markjenkins.ca>

from binascii import unhexlify
from string import hexdigits

from .key_from_random import make_key_building_from_existing_bytes_plus_urandom

def make_key_from_hex_strings(hex_strings):
    return make_key_building_from_existing_bytes_plus_urandom(
        unhexlify( bytes(''.join(hex_strings), 'ascii') )
        )

def make_key_from_hex_prompt():
    hex_line = ''.join(
        character
        for character in input(
            "Enter some hex as additional entropy, needs to be an even number "
            "of hex characters\n> ")
        if character in hexdigits
        )
    print("thanks, got %i bytes (%i bits) out of that" % (
            len(hex_line) // 2, len(hex_line) * 8 // 2) )
    print()
    return make_key_from_hex_strings( (hex_line,) )
