
#!/usr/bin/env python3
# Python 3 only, does not have backwards compatible support for Python 2

# Copyright Mark Jenkins, 2013
#
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved. This file is offered as-is,
# without any warranty.
# http://www.gnu.org/prep/maintain/html_node/License-Notices-for-Other-Files.html
# @author Mark Jenkins <mark@markjenkins.ca>

from os import urandom

from ecdsa.curves import SECP256k1
from ecdsa.keys import SigningKey
from ecdsa.util import randrange

def return_empty_tuple(*args, **kargs):
    return ()

try:
    from .dice import return_byte_decoded_dice_from_prompt
    from .dice import dice_decode
except ImportError:
    return_byte_decoded_dice_from_prompt = return_empty_tuple
    dice_decode = return_empty_tuple

def gen_composite_entropy_func(*args):
    def pump_out_bytes(sources, byte_count):
        for source in sources:
            out_bytes = source(byte_count)
            yield out_bytes
            byte_count -= len(out_bytes)
            if byte_count <= 0:
                break
    def composed_entropy_func(bytes_required):
        return b''.join(pump_out_bytes(args,  bytes_required))
    return composed_entropy_func

def make_key_from_entropy_source(entropy=None):
    return SigningKey.generate(SECP256k1, entropy=entropy) 

make_key_from_OS = make_key_from_entropy_source

def make_key_building_from_existing_bytes_plus_urandom(existing_bytes):
    return make_key_from_entropy_source(
        gen_composite_entropy_func(
            lambda x: existing_bytes,
            urandom )
        )

def make_key_from_dice_rolls_provided(dice_rolls):
    return make_key_building_from_existing_bytes_plus_urandom(
        dice_decode(dice_rolls) )

def make_key_from_dice_rolls_prompt():
    return make_key_building_from_existing_bytes_plus_urandom(
        return_byte_decoded_dice_from_prompt() )

def show_wallet_xor_scheme(private_key_bytes):
    pass
