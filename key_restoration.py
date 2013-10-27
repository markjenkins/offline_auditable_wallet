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

from oaw.wif import (
    wif_to_private_key_and_public_compressed, private_key_to_wif,
    )
from oaw.rfc_1760_dict_encode import words_iter_to_32_bytes
from oaw.bitcoin_address import private_key_bytes_to_bitcoin_address

def command_line_main():
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
