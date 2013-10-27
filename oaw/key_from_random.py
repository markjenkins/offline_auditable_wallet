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

from ecdsa.curves import SECP256k1
from ecdsa.keys import SigningKey

def make_key_from_OS():
    return SigningKey.generate(SECP256k1) 

def make_key_from_dice_rolls():
    # should use SingingKey.generate with dice rolls providing initial entropy
    # and os.urandom the rest
    #
    pass

def make_key_from_hex_string():
    # should use SingingKey.generate with this hex initial entropy
    # and os.urandom the rest
    pass

def show_wallet_xor_scheme(private_key_bytes):
    pass
