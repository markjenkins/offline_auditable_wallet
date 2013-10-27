from .encoding import (
    create_reverse_dictionary, sym_decode, sym_encode_with_zero_pad,
    )

DICTIONARY = tuple(
    '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz' )
REVERSE_DICTIONARY = create_reverse_dictionary(DICTIONARY)

def b58decode(v, length=None):
    return sym_decode(v, REVERSE_DICTIONARY, length)

def b58encode(v):
    return ''.join(sym_encode_with_zero_pad(v, DICTIONARY))

