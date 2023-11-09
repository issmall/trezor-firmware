from trezor.crypto.base58 import encode_check, decode_check
from trezor.crypto.hashlib import sha3_256


def get_address_from_public_key(pubkey):
    return encode_check(b'\x41' + sha3_256(pubkey[1: 65], keccak=True).digest()[12: 32])

def address_to_bytes(address):
    return decode_check(address)
