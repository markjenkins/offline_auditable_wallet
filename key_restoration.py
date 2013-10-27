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

try:
    from rfc_1760_dict_encode import restore_dict_encoded_key
except ImportError:
    restore_dict_encoded_key = missing_menu_item

def restore_xor_scheme_key_menu():
    pass

def restore_key_from_seed_menu():
    pass

def restore_key_from_passphrase_menu():
    pass

def private_key_bytes_to_bitcoin_address(
    private_key_bytes, compressed_public_key):
    signing_key = SigningKey.from_string(private_key_bytes, SECP256k1)
    return get_bitcoin_address_from_signing_key(
        signing_key, compressed_public_key)

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
        print(
            "The bitcoin address is %s" %
            private_key_bytes_to_bitcoin_address(private_key_bytes, compressed)
            )
    else:
        print("problem with imported key")

def command_line_main():
    from optparse import OptionParser
    from wif import (
        wif_to_private_key_and_public_compressed, private_key_to_wif,
        )
    from rfc_1760_dict_encode import words_iter_to_32_bytes

    parser = OptionParser()
    parser.add_option(
        "-W", "--wif",
        dest="input_format",
        action="store_const", const="W",
        help="input new key in wallet import format (WIF)",
        default='W',
        )
    parser.add_option(
        "--rfc",
        dest="input_format",
        action="store_const",
        const="rfc",
        )

    (options, args) = parser.parse_args()
    private_key_convert = {
        'W': lambda a: wif_to_private_key_and_public_compressed(a[0]),
        'rfc': lambda a: (words_iter_to_32_bytes(a), True),
        }

    private_key_bytes, compressed = \
        private_key_convert[options.input_format](args)
    print(private_key_to_wif(private_key_bytes, compressed))
    print(private_key_bytes_to_bitcoin_address(private_key_bytes, compressed))

if __name__ == "__main__":
    command_line_main()
