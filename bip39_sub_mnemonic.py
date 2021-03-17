#!/usr/bin/env python3

from sys import stderr
from oaw.bip39 import (
    seed_from_mnemonic_and_passphrase, bytes_to_bip39_w_checksum,
    bip39_words_to_bytes,
    )

# One of the sins of cryptography is inventing your own cryptography
#
# That's what's going on here, so you should only review the idea, and
# not adopt this.
#
# At least there is one bit of non-invention going on here. We derrive a
# sub-mnemonic using the same key derivation cryptography bip39 specifies
# for generating a binary seed from a mnemonic
#
# In the case of a weak passphrase, someone knowing the master mnemonic
# will be able to derive the sub mnemonic, as long as they know the algorithm
# and the derivation passphrase. That's the intention.
#
# The part that's harder to show is the idea that a sub-mnemonic shouldn't
# reveal information about the master mnemonic, regardless of the derivation
# passphrase. This one-wayness is the idea behind cryptographic hash algorithms
#
# The goal is to entrust the sub-mnemonics to wallets we wouldn't trust with
# the master mnemonic, which can reduce the number of mnemonics that need to
# be retained. In practice, the derivation method and passphrase still needs
# to be retained, and for something so experimental the generated sub-mnemonic
# should really be backed up as well.

print(
    """WARNING, this idea of sub-mnemonics is not standard in the """
    """bitcoin/cryptocurrency world. This is non-standard and """
    """has not recieved a security audit. Using this could cause """
    """lost funds and is not recommended. See additional notes in source.

This has been published for review purposes, not production use.""",
    file=stderr)

master_mnemonic = input("master mnemonic> ").strip()
master_mnemonic_bytes = bip39_words_to_bytes(master_mnemonic)

sub_mnemonic_passphrase = input("sub-mnemonic passphrase> ").strip()

sub_mnemonic_seed = seed_from_mnemonic_and_passphrase(
    master_mnemonic,
    sub_mnemonic_passphrase)

sub_mnemonic_seed_truncated = sub_mnemonic_seed[:len(master_mnemonic_bytes)]
print( bytes_to_bip39_w_checksum( sub_mnemonic_seed_truncated ))
