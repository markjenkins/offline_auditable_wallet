#!/usr/bin/env python3

from random import randrange

from ecdsa.six import int2byte

from oaw.base58 import (
    b58decode as b58decode_mine,
    b58encode as b58encode_mine
    )

# for comparison, the following is a python 3 ported version of 
# Gavin Andreson's base58 decode/encode in python
# https://bitcointalk.org/index.php?topic=1026.0

__b58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
__b58base = len(__b58chars)

def b58encode(v):
	""" encode v, which is a string of bytes, to base58.
	"""
	long_value = 0
	for (i, c) in enumerate(v[::-1]):
		long_value += (256**i) * c

	result = ''
	while long_value >= __b58base:
		div, mod = divmod(long_value, __b58base)
		result = __b58chars[mod] + result
		long_value = div
	result = __b58chars[long_value] + result

	# Bitcoin does a little leading-zero-compression:
	# leading 0-bytes in the input become leading-1s
	nPad = 0
	for c in v:
		if c == 0: nPad += 1
		else: break

	return (__b58chars[0]*nPad) + result

def b58decode(v, length):
	""" decode v into a string of len bytes
	"""
	long_value = 0
	for (i, c) in enumerate(v[::-1]):
		long_value += __b58chars.find(c) * (__b58base**i)

	result = b''
	while long_value >= 256:
		div, mod = divmod(long_value, 256)
		result = int2byte(mod) + result
		long_value = div
	result = int2byte(long_value) + result

	nPad = 0
	for c in v:
		if c == __b58chars[0]: nPad += 1
		else: break

	result = b'\x00'*nPad + result
	if length is not None and len(result) != length:
		return None

	return result

def get_test_random_bytes(num_bytes):
    return bytes( randrange(2 ** 8)
                  for i in range(num_bytes)
                  )

def test():
    # special case, we should have one leading 0 symbol for
    # every leading 0 byte
    lead_zero_bytes = b'\x00\x00\x32'
    b58 = b58encode_mine(lead_zero_bytes)
    assert b58 == b58encode(lead_zero_bytes )
    assert b58decode_mine(b58, len(lead_zero_bytes)) == lead_zero_bytes, \
        "%s %s" % (lead_zero_bytes, b58decode_mine(b58, len(lead_zero_bytes) ))

    for j in range(9000):
        for i in range(1, 3+1):
            random_bytes = get_test_random_bytes(i)

            b58_mine = b58encode_mine(random_bytes)    
            b58 = b58encode(random_bytes)

            # different handling for test cases where every byte is zero
            # I manage to put a matching number of 0 symbols to encode
            # these leading zeros with the same number of characters
            #
            # Gavin puts out an extra 0 symbol
            if all(0 == a for a in random_bytes):
                assert b58decode_mine(b58_mine, i) == random_bytes
                assert len(b58) == len(b58_mine)+1

                # the Gavin routines don't seem to be able to handle decoding
                # all zeros at all, either how it encodes them or how I
                # encode them
                # assert b58decode(b58, i) == random_bytes
                # assert b58decode(b58_mine, i) == random_bytes

                # but I can handle Gavin's longer encoding just fine too
                assert b58decode_mine(b58, i) == random_bytes
            # the rest of the time, Gavin and I are in full agreement
            else:
                assert b58 == b58_mine
                assert b58decode_mine(b58, i) == random_bytes
                assert b58decode(b58, i) == random_bytes

if __name__ == "__main__":
    test()
