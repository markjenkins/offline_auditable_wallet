# Copyright Mark Jenkins, 2013
#
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved. This file is offered as-is,
# without any warranty.
# http://www.gnu.org/prep/maintain/html_node/License-Notices-for-Other-Files.html
# @author Mark Jenkins <mark@markjenkins.ca>

from ecdsa.keys import SigningKey

from .menu import (
    run_menu, do_menu_run, always_return_false, missing_menu_item)

from .key_from_random import (
    make_key_from_entropy_source,
    )
from .bitcoin_address import get_bitcoin_address_from_signing_key

try:
    from .wif import show_wallet_import_format
except ImportError:
    show_wallet_import_format = missing_menu_item

try:
    from .rfc_1760_dict_encode import show_wallet_dict_words
except ImportError:
    show_wallet_dict_words = missing_menu_item

try:
    from .xor import show_wallet_xor_scheme
except ImportError:
    show_wallet_xor_scheme = missing_menu_item

from .entropy import get_entropy_source_menu

def display_private_key_menu(signing_key):
    # always generate bitcon addresses based on the compressed public key
    compressed = True

    run_menu(
        "Super, how do you want to display this private key for safekeeping?\n"
        "Would like like to display it in (W)allet import format, "
        "encode it with some (D)ictionary words, "
        "display a 2 of 3 (X)or scheme, or (E)xit?",
        ( ("W", show_wallet_import_format),
          ("D", show_wallet_dict_words),
          ("X", show_wallet_xor_scheme),
          ("E", always_return_false),
          ),
        signing_key.to_string(),
        compressed
        )    

    bitcoin_address = get_bitcoin_address_from_signing_key(signing_key,
                                                           compressed)
    print("Your public bitcoin address is %s" % bitcoin_address)
    print()

def run_key_gen_menu():
    entropy_source = get_entropy_source_menu()
    if entropy_source is False:
        return False
    private_key = make_key_from_entropy_source(entropy_source)
    if isinstance(private_key, SigningKey):
        display_private_key_menu(private_key)

def run_seed_gen_menu():
    # we'll do funky stuff like SigningKey.from_secret_exponent(
    #   randrange_from_seed__trytryagain )
    # 
    pass

def run_passphrase_menu():
    pass

def generate_key_menu():
    key = run_menu(
        "How do you want to generate your key?\n"
        "Do you want to randomly generate a private (K)ey and print it, "
        "randomly generate a (S)eed, supply a (P)assphrase, "
        "or E(xit) to the main menu?",
        ( ('K', run_key_gen_menu),
          ('S', run_seed_gen_menu),
          ('P', run_passphrase_menu),
          ('E', always_return_false),
          )
        )
