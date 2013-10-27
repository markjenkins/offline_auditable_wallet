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

from oaw.menu import (
    run_menu, do_menu_run, always_return_false, missing_menu_item)
from oaw.bitcoin_address import get_bitcoin_address_from_signing_key

try:
    from oaw.wif import show_wallet_import_format
except ImportError:
    show_wallet_import_format = missing_menu_item

try:
    from oaw.rfc_1760_dict_encode import show_wallet_dict_words
except ImportError:
    show_wallet_dict_words = missing_menu_item

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
    private_key = do_menu_run(
        "We need some random data for this.\n"
        "Do you fully trust the crypto grade (R)andom number generator from "
        "your operating system? (/dev/urandom on Unix-like systems, "
        "CryptGenRandom() on Windows)\n"
        "Or, would you like to supplement it with some entropy of your own "
        "by rolling some six sided (D)ice or "
        "provide bytes from whatever other random source you "
        "trust in (H)ex? "
        "You can also (E)xit.",
        ( ('R', make_key_from_OS),
          ('D', make_key_from_dice_rolls),
          ('H', make_key_from_hex_string),
          ('E', always_return_false),
          )
        )
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

def command_line_main():
    from optparse import OptionParser
    from oaw.wif import private_key_to_wif
    from oaw.rfc_1760_dict_encode import joined_words_for_bytes

    parser = OptionParser()
    parser.add_option(
        "-W", "--wif",
        dest="output_format",
        action="store_const", const="W",
        help="output new key in wallet import format (WIF)",
        default='W',
        )
    parser.add_option(
        "--rfc",
        dest="output_format",
        action="store_const",
        const="rfc",
        )

    (options, args) = parser.parse_args()
    signing_key = make_key_from_OS()
    compressed_public_key = True

    private_key_display = {
        'W': lambda x: private_key_to_wif(x, compressed_public_key),
        'rfc': joined_words_for_bytes,
        }
    print( private_key_display[options.output_format](
            signing_key.to_string() ) )
    print( get_bitcoin_address_from_signing_key(
            signing_key, compressed_public_key ))

if __name__ == "__main__":
    command_line_main()
