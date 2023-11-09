from trezor.crypto.base58 import encode_check, decode_check
from trezor.messages import TronSignTx

from apps.common.writers import write_bytes_fixed

TYPE_VARINT = 0
TYPE_DOUBLE = 1
TYPE_STRING = 2
TYPE_GROUPS = 3
TYPE_GROUPE = 4
TYPE_FLOAT = 5


def add_field(w, fnumber, ftype):
    if fnumber > 15:
        w.append(fnumber << 3 | ftype)
        w.append(0x01)
    else:
        w.append(fnumber << 3 | ftype)

def write_varint(w, value):
    while True:
        byte = value & 0x7f
        value = value >> 7
        if value == 0:
            w.append(byte)
            break
        else:
            w.append(byte | 0x80)

def write_bytes_with_length(w, buf: bytes):
    write_varint(w, len(buf))
    write_bytes_fixed(w, buf, len(buf))

def pack_contract(contract, owner_address):
    retc = bytearray()
    add_field(retc, 1, TYPE_VARINT)
    cmessage = bytearray()
    api = ''
    if contract.transfer_contract:
        write_varint(retc, 1)
        api = 'TransferContract'
        add_field(cmessage, 1, TYPE_STRING)
        write_bytes_with_length(cmessage, decode_check(owner_address))
        add_field(cmessage, 2, TYPE_STRING)
        write_bytes_with_length(cmessage, decode_check(contract.transfer_contract.to_address))
        add_field(cmessage, 3, TYPE_VARINT)
        write_varint(cmessage, contract.transfer_contract.amount)

    if contract.trigger_smart_contract:
        write_varint(retc, 31)
        api = 'TriggerSmartContract'
        add_field(cmessage, 1, TYPE_STRING)
        write_bytes_with_length(cmessage, decode_check(owner_address))
        add_field(cmessage, 2, TYPE_STRING)
        write_bytes_with_length(cmessage, decode_check(contract.trigger_smart_contract.contract_address))

        if contract.trigger_smart_contract.call_value:
            add_field(cmessage, 3, TYPE_VARINT)
            write_varint(cmessage, contract.trigger_smart_contract.call_value)

        add_field(cmessage, 4, TYPE_STRING)
        write_bytes_with_length(cmessage, contract.trigger_smart_contract.data)

        if contract.trigger_smart_contract.call_token_value:
            add_field(cmessage, 5, TYPE_VARINT)
            write_varint(cmessage, contract.trigger_smart_contract.call_token_value)
            add_field(cmessage, 6, TYPE_VARINT)
            write_varint(cmessage, contract.trigger_smart_contract.asset_id)

    capi = bytearray()
    add_field(capi, 1, TYPE_STRING)
    write_bytes_with_length(capi, bytes('type.googleapis.com/protocol.' + api, 'ascii'))

    add_field(capi, 2, TYPE_STRING)
    write_bytes_with_length(capi, cmessage)

    add_field(retc, 2, TYPE_STRING)
    write_bytes_with_length(retc, capi)
    return retc


def serialize(transaction: TronSignTx, owner_address: str):
    ret = bytearray()
    add_field(ret, 1, TYPE_STRING)
    write_bytes_with_length(ret, transaction.ref_block_bytes)
    add_field(ret, 4, TYPE_STRING)
    write_bytes_with_length(ret, transaction.ref_block_hash)
    add_field(ret, 8, TYPE_VARINT)
    write_varint(ret, transaction.expiration)
    if transaction.data is not None:
        add_field(ret, 10, TYPE_STRING)
        write_bytes_with_length(ret, bytes(transaction.data, 'ascii'))

    retc = pack_contract(transaction.contract, owner_address)

    add_field(ret, 11, TYPE_STRING)
    write_bytes_with_length(ret, retc)
    add_field(ret, 14, TYPE_VARINT)
    write_varint(ret, transaction.timestamp)
    if transaction.fee_limit:
        add_field(ret, 18, TYPE_VARINT)
        write_varint(ret, transaction.fee_limit)

    return ret
