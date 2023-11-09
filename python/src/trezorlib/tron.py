from typing import TYPE_CHECKING, AnyStr

from . import messages
from .tools import expect, prepare_message_bytes


if TYPE_CHECKING:
    from .client import TrezorClient
    from .tools import Address
    from .protobuf import MessageType

@expect(messages.TronAddress, field='address', ret_type=str)
def get_address(
        client: "TrezorClient",
        address_n: "Address",
        show_display: bool = False,
) -> "MessageType":
    return client.call(
        messages.TronGetAddress(address_n=address_n, show_display=show_display)
    )

@expect(messages.TronMessageSignature)
def sign_message(
        client: 'TrezorClient',
        n: 'Address',
        message: AnyStr,
) -> 'MessageType':
    return client.call(
        messages.TronSignMessage(
            address_n=n,
            message=prepare_message_bytes(message),
        ),
    )

@expect(messages.TronSignedTx)
def sign_tx(
        client: 'TrezorClient',
        address_n: 'Address',
        msg: messages.TronSignTx,
) -> 'MessageType':
    msg.address_n = address_n
    return client.call(msg)
