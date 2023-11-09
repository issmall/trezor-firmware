from typing import TYPE_CHECKING

from trezor.crypto.curve import secp256k1
from trezor.ui.layouts import show_address
from trezor.messages import TronAddress, TronGetAddress

from apps.common import paths
from apps.common.keychain import Keychain, auto_keychain
from apps.tron.address import get_address_from_public_key

from . import PATTERN, SLIP44_ID

@auto_keychain(__name__)
async def get_address(
    msg: TronGetAddress, keychain: Keychain
) -> TronAddress:
    await paths.validate_path(keychain, msg.address_n)

    node = keychain.derive(msg.address_n)
    seckey = node.private_key()
    public_key = secp256k1.publickey(seckey, False)
    address = get_address_from_public_key(public_key[:65])

    if msg.show_display:
        path = paths.address_n_to_str(msg.address_n)
        await show_address(
            address=address,
            path=path,
            account=paths.get_account_name('TRX', msg.address_n, PATTERN, SLIP44_ID),
            network='Tron',
        )

    return TronAddress(address=address)
