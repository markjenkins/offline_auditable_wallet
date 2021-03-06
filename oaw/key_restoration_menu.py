# Copyright Mark Jenkins, 2013
#
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved. This file is offered as-is,
# without any warranty.
# http://www.gnu.org/prep/maintain/html_node/License-Notices-for-Other-Files.html
# @author Mark Jenkins <mark@markjenkins.ca>

from .menu import do_menu_run, always_return_false, missing_menu_item
from .bitcoin_address import private_key_bytes_to_bitcoin_address

try:
    from .wif import restore_wif_key
except ImportError:
    restore_wif_key = missing_menu_item

try:
    from .rfc_1760_dict_encode import restore_dict_encoded_key
except ImportError:
    restore_dict_encoded_key = missing_menu_item

try:
    from .xor import restore_xor_scheme_menu
except ImportError:
    restore_xor_scheme_menu = missing_menu_item

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
          ('X', restore_xor_scheme_menu),
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

