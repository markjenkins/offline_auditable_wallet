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

from optparse import OptionParser

from oaw.bitcoin_address import get_bitcoin_address_from_signing_key
from oaw.wif import private_key_to_wif
from oaw.rfc_1760_dict_encode import joined_words_for_bytes
from oaw.key_from_random import (
    make_key_from_OS, make_key_from_dice_rolls_provided,
    )
from oaw.hex import make_key_from_hex_strings

def command_line_main():
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
    parser.add_option(
        "-D", "--dice",
        dest="random_source",
        action="store_const", const="D",
        default="OS",
        )
    parser.add_option(
        "-H", "--hex",
        dest="random_source",
        action="store_const", const="H", )

    (options, args) = parser.parse_args()

    signing_key = { 'OS': lambda x: make_key_from_OS(),
                    'D': make_key_from_dice_rolls_provided,
                    'H': make_key_from_hex_strings,
                    }[options.random_source](args)
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
