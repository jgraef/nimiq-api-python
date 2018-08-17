__all__ = ["satoshi_to_coin", "coin_to_satoshi", "ensure_satoshi", "block_listener"]

import logging

from decimal import Decimal
from time import sleep
from typing import Union

logger = logging.getLogger(__name__)


SATOSHI_PER_COIN = 100000


def satoshi_to_coin(satoshi: int) -> Decimal:
    """
    Converts a value in Satoshis into Coins (NIMs).
    :param satoshi: The value in Satoshis as int
    :return: The value in coins as Decimal
    """
    return Decimal(satoshi) / SATOSHI_PER_COIN


def coin_to_satoshi(coin: Decimal) -> int:
    """
    Converts a value in Coins (NIMs) into Satoshis
    :param coin: The value in coins as Decimal
    :return: The value in Satoshi as int
    """
    return int(coin * SATOSHI_PER_COIN)


def ensure_satoshi(value: Union[int, Decimal]) -> int:
    """
    Ensures the returned value is in Satoshi. If the value was an int, it's already in Satoshi. If the value was an
    Decimal, it was in Coins and will be converted.
    :param value: The value in Satoshis (int) or Coins (Decimal).
    :return: The value in Satoshis (int)
    """
    if type(value) == Decimal:
        return coin_to_satoshi(value)
    elif type(value) == int:
        return value
    else:
        raise ValueError("Expected value to be either int or Decimal")


def block_listener(nimiq, first_block = None):
    """
    An interable that yields blocks as they are added to the block chain.
    :param nimiq: The Nimiq API
    :return: The iterable that yields new blocks.
    """
    if first_block is None:
        height = nimiq.block_number()
    else:
        height = first_block
    while True:
        block = nimiq.get_block_by_number(height)
        if block is None:
            sleep(1)
        else:
            yield block
            height += 1
