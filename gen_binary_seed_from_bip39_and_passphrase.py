#!/usr/bin/env python3

from oaw.bip39 import seed_from_mnemonic_and_passphrase

mnemonic = input("mnemonic> ").strip()
passphrase = input("passphrase> ").strip()

print( seed_from_mnemonic_and_passphrase(mnemonic, passphrase).hex() )
