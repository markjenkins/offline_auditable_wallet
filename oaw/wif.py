# Copyright Mark Jenkins, 2013
#
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved. This file is offered as-is,
# without any warranty.
# http://www.gnu.org/prep/maintain/html_node/License-Notices-for-Other-Files.html
# @author Mark Jenkins <mark@markjenkins.ca>

from .pywallet_abridged import SecretToASecret, ASecretToSecret, is_compressed

def private_key_to_wif(private_key_bytes, compressed_public):
    return SecretToASecret( private_key_bytes, compressed_public)

def show_wallet_import_format(private_key_bytes, compressed_public):
    print("Your private key is:")
    print( private_key_to_wip(private_key_bytes, compressed_public) )
    return False

def wif_to_private_key_and_public_compressed(wif):
    # we're only interested in the first 32 bytes, there might be an
    # extra one from this being a private key that co-responds to a
    # compressed public key based bitcoin address but we don't need it
    return ASecretToSecret(wif)[:32], is_compressed(wif)    

def restore_wif_key():
    return wif_to_private_key_and_public_compressed(
        input("Enter wallet import format. > ") )
