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

from .pywallet_abridged import \
    (GetPubKey, public_key_to_bc_address,
     )

def private_key_bytes_to_bitcoin_address(
    private_key_bytes, compressed_public_key):
    signing_key = SigningKey.from_string(private_key_bytes, SECP256k1)
    return get_bitcoin_address_from_signing_key(
        signing_key, compressed_public_key)

def get_bitcoin_address_from_signing_key(
    signing_key, compressed_public_key):
    return public_key_to_bc_address(
        GetPubKey(signing_key.get_verifying_key(), compressed_public_key)
        )
