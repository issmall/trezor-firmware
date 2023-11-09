import json
import click

from typing import TYPE_CHECKING, TextIO

from .. import messages, protobuf, tools, tron
from . import with_client

if TYPE_CHECKING:
    from ..client import TrezorClient


PATH_HELP = "BIP-32 path, e.g. m/44'/195'/0'/0/0"

@click.group(name='tron')
def cli():
    '''Tron commands'''

@cli.command()
@click.option('-n', '--address', required=True, help=PATH_HELP)
@click.option('-d', '--show-display', is_flag=True)
@with_client
def get_address(client: "TrezorClient", address: str, show_display: bool):
    address_n = tools.parse_path(address)
    return tron.get_address(client, address_n, show_display)

@cli.command()
@click.option('-n', '--address', required=True, help=PATH_HELP)
@click.argument('message')
@with_client
def sign_message(
        client: 'TrezorClient',
        address: str,
        message: str,
) -> dict:
    address_n = tools.parse_path(address)
    ret = tron.sign_message(client, address_n, message)
    output = {
        'message': message,
        'address': ret.address,
        'signature': ret.signature.hex(),
    }
    return output
