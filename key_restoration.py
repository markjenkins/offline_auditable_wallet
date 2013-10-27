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

from ecdsa.keys import SigningKey
from ecdsa.curves import SECP256k1

from menu import do_menu_run, always_return_false
from bitcoin_address import get_bitcoin_address_from_signing_key

try:
    from wif import restore_wif_key
except ImportError:
    restore_wif_key = missing_menu_item

def restore_dict_encoded_key():
    pass

def restore_xor_scheme_key_menu():
    pass

def restore_key_from_seed_menu():
    pass

def restore_key_from_passphrase_menu():
    pass

def restore_key_menu():
    (private_key_bytes, compressed) = do_menu_run(
        "Is your key in (W)allet import format, "
        "encoding with words from a (D)ictionary, "
        "encoded with a 2 of 3 (X)or scheme, "
        "generated from a (S)eed, "
        "derived from a (P)assphrase or "
        "(E)xit to the main menu?",
        ( ('W', restore_wif_key),
          ('D', restore_dict_encoded_key),
          ('X', restore_xor_scheme_key_menu),
          ('S', restore_key_from_seed_menu),
          ('P', restore_key_from_passphrase_menu),
          ('E', always_return_false),
         )
        )
    if isinstance(private_key_bytes, bytes):
        signing_key = SigningKey.from_string(private_key_bytes, SECP256k1)
        print("The bitcoin address is %s" %
              get_bitcoin_address_from_signing_key(signing_key, compressed))
    else:
        print("problem with imported key")

if __name__ == "__main__":
    restore_key_menu()
