from trezor import wire
from trezor.crypto.base58 import encode_check
from trezor.crypto.curve import secp256k1
from trezor.crypto.hashlib import sha256
from trezor.messages import TronSignTx, TronSignedTx

from apps.common import paths
from apps.common.keychain import Keychain, auto_keychain
from apps.tron.address import get_address_from_public_key
from apps.tron.serialize import serialize

from . import layout, tokens

def validate(msg: TronSignTx):
    if None in (msg.contract,):
        raise wire.ProcessError('contract required')


async def _require_confirm_by_type(transaction, owner_address):
    if transaction.data:
        await layout.require_confirm_data(transaction.data, len(transaction.data))

    contract = transaction.contract
    if contract.transfer_contract:
        if contract.transfer_contract.amount is None:
            raise wire.DataError('invalid amount')

        await layout.require_confirm_tx(
            contract.transfer_contract.to_address,
            contract.transfer_contract.amount,
        )
    elif contract.trigger_smart_contract:
        data = contract.trigger_smart_contract.data
        if data is None:
            raise wire.DataError('invalid contract call data')

        func_sig = hexlify(data[: 4])

        if func_sig == b'a9059cbb': # transfer
            token = tokens.token_by_address(
                'TRC20', contract.trigger_smart_contract.contract_address
            )
            recipient = encode_check(b'\x41' + data[16: 36])
            value = int.from_bytes(data[36: 68], 'big')
            await layout.require_confirm_trigger_trc20(
                False if token is tokens.UNKNOWN_TOKEN else True,
                contract.trigger_smart_contract.contract_address,
                value,
                token,
                recipient,
            )
            if transaction.fee_limit:
                await layout.require_confirm_fee(
                    token,
                    from_address=owner_address,
                    to_address=recipient,
                    value=value,
                    fee_limit=transaction.fee_limit,
                )
        else:
            raise wire.DataError('invalid func')


@auto_keychain(__name__)
async def sign_tx(
        msg: TronSignTx, keychain: Keychain
) -> TronSignedTx:
    validate(msg)
    address_n = msg.address_n or ()
    await paths.validate_path(keychain, msg.address_n)
    node = keychain.derive(address_n)

    seckey = node.private_key()
    public_key = secp256k1.publickey(seckey, False)
    address = get_address_from_public_key(public_key[: 65])
    try:
        await _require_confirm_by_type(msg, address)
    except AttributeError as e:
        raise wire.DataError('invalid asset data field')

    owner_address = address

    if msg.contract.transfer_contract:
        owner_address = msg.contract.transfer_contract.owner_address or owner_address
    elif msg.contract.trigger_smart_contract:
        owner_address = msg.contract.trigger_smart_contract.owner_address or owner_address

    raw_data = serialize(msg, owner_address)
    data_hash = sha256(raw_data).digest() # txID
    signature = secp256k1.sign(seckey, data_hash, False)
    signature = signature[1: 65] + bytes([(~signature[0] & 0x01) + 27])
    return TronSignedTx(signature=signature, serialized_tx=raw_data)
