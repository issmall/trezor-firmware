from trezor.crypto.curve import secp256k1
from trezor.crypto.hashlib import sha3_256
from trezor.messages import TronMessageSignature, TronSignMessage
from trezor.ui.layouts import confirm_signverify
from trezor.utils import HashWriter

from apps.common import paths
from apps.common.keychain import Keychain, auto_keychain
from apps.common.signverify import decode_message
from apps.tron.address import get_address_from_public_key


def message_digest(message: bytes) -> bytes:
    h = HashWriter(sha3_256(keccak=True))
    signed_message_header = b'\x19TRON Signed Message:\n'
    h.extend(signed_message_header)
    h.extend(str(len(message)).encode())
    h.extend(message)
    return h.get_digest()

@auto_keychain(__name__)
async def sign_message(
        msg: TronSignMessage, keychain: Keychain
) -> TronMessageSignature:
    address_n = msg.address_n or ()
    await paths.validate_path(keychain, msg.address_n)
    node = keychain.derive(address_n)

    seckey = node.private_key()
    public_key = secp256k1.publickey(seckey, False)
    address = get_address_from_public_key(public_key[:65])
    print(address)
    await confirm_signverify(
        decode_message(msg.message), address, verify=False,
    )

    signature = secp256k1.sign(
        node.private_key(),
        message_digest(msg.message),
        False,
        secp256k1.CANONICAL_SIG_ETHEREUM,
    )

    return TronMessageSignature(
        address=bytes(address, 'ascii'),
        signature=signature[1:] + bytearray([signature[0]]),
    )
