# from typing import TYPE_CHECKING
from trezor.enums import ButtonRequestType
from trezor.strings import format_amount
from trezor.ui.layouts import confirm_address, confirm_output, confirm_blob, confirm_ethereum_tx
from . import tokens

# if TYPE_CHECKING:
from typing import Awaitable

def format_amount_trx(value: int, token: tokens.TokenInfo | None) -> str:
    if token:
        suffix = token.symbol
        decimals = token.decimals
    else:
        suffix = 'TRX'
        decimals = 6

    return f'{format_amount(value, decimals)} {suffix}'

def require_confirm_fee(
        token: tokens.TokenInfo | None = None,
        from_address: str | None = None,
        to_address: str | None = None,
        value: int = 0,
        fee_limit: int = 0,
) -> Awaitable[None]:
    if token is None:
        total_amount = format_amount_trx(value + fee_limit, None)
    else:
        total_amount = None

    return confirm_ethereum_tx(
        to_address,
        format_amount_trx(value, token),
        format_amount_trx(fee_limit, None),
        items=(('', ''), ),
        br_code=ButtonRequestType.SignTx,
    )


def require_confirm_trigger_trc20(
        verified: bool,
        contract_address: str,
        amount: int,
        token: tokens.TokenInfo,
        to_address: str,
) -> Awaitable[None]:
    if verified:
        return confirm_output(
            address=to_address,
            amount=format_amount_trx(amount, token),
            br_code=ButtonRequestType.SignTx,
        )

    return confirm_address(
        'unknown token',
        contract_address,
        'Contract:',
        'unknown_token',
        br_code=ButtonRequestType.SignTx,
    )


def require_confirm_tx(to: str, value: int) -> Awaitable[None]:
    to_str = to
    return confirm_output(
        address=to_str,
        amount=format_amount_trx(value, None),
        hold=True,
        br_code=ButtonRequestType.SignTx,
    )



def require_confirm_data(data: bytes, data_total: int) -> Awaitable[None]:
    return confirm_blob(
        'confirm_data',
        'confirm_data',
        data,
        f'Size: {data_total} bytes',
        br_code=ButtonRequestType.SignTx,
        ask_pagination=True,
    )
