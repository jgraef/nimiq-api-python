__all__ = ["NimiqApi"]

from binascii import hexlify, unhexlify

from decimal import Decimal
from typing import Union

from .jsonrpc import JsonRpcClient
from .util import satoshi_to_coin, ensure_satoshi


class NimiqApi:
    """
    API client for the Nimiq JSON RPC server.

    Examples:

       >>> nimiq = NimiqApi()
       >>> nimiq.get_block_by_number(0)
       {'accountsHash': 'c5ec6638e93eda82c1221c24083f9c6b0d85b227c1d14ead5e595eb3c4f272db',
        'bodyHash': '8223886130688ca40f9812eae66b0280e6ce2f72a743d08aac819be475b3ec4f',
        'difficulty': 1,
        'extraData': '',
        'hash': 'ca49936f6db63cad7cf73eb1e9da53dd497ad3b7068f31731024785973be9be6',
        'miner': '0000000000000000000000000000000000000000',
        'minerString': 'NQ07 0000 0000 0000 0000 0000 0000 0000 0000',
        'nonce': 104295,
        'number': 1,
        'parentHash': '0000000000000000000000000000000000000000000000000000000000000000',
        'pow': '00009505db53818e41456a83f79c19fe47a485bd6a486ac4accdef3ca8cde937',
        'size': 173,
        'timestamp': 0,
        'transactions': []}

       >>> nimiq.accounts()
       [{'id': 'f1ac032bfe0814331d2a57ce74f346c6c75b4eb6', 'address': 'NQ76 X6N0 6AYX 10A3 679A AY77 9US6 QT3M NKMN'},
        {'id': '8629c69a857f715aff9a6e5b084eaa15af7730b2', 'address': 'NQ53 GQLU D6L5 FVQM MYUS DRDG GKMA 2NPP EC5J'}]

       >>> nimiq.get_balance("NQ53 GQLU D6L5 FVQM MYUS DRDG GKMA 2NPP EC5J")
       Decimal('83503.27457')

       >>> nimiq.send_transaction("NQ53 GQLU D6L5 FVQM MYUS DRDG GKMA 2NPP EC5J", \
                                  "NQ76 X6N0 6AYX 10A3 679A AY77 9US6 QT3M NKMN", \
                                   100000, 10)
       '74cee0799277e9f58bf558329ac64bb75ef432e6ca685e4d8986517204a148cf'

    """

    def __init__(self, url="http://localhost:8648"):
        """
        :param url: URL to RPC endpoint (default: ``http://localhost:8648``)
        """
        self._rpc = JsonRpcClient(url)

    def send_raw_transaction(self, tx: bytes):
        """
        Sends a raw transaction
        :param tx: Raw transaction (as bytes)
        :return: Transaction hash (as hex string)
        """
        return self._rpc.call("sendRawTransaction", hexlify(tx).decode())

    def send_transaction(self, from_addr: str, to_addr: str, value: Union[int, Decimal], fee: Union[int, Decimal]):
        """
        Sends a transaction
        :param from_addr: Sender address
        :param to_addr: Receiver address
        :param value: Value in Satoshis (int) or NIMs (Decimal)
        :param fee: Fee in Satoshis (int) or NIMs (Decimal)
        :return: Transaction hash
        """
        return self._rpc.call("sendTransaction", {
            "from": from_addr,
            "to": to_addr,
            "value": ensure_satoshi(value),
            "fee": ensure_satoshi(fee),
        })


    def get_transaction_by_hash(self, hash: str):
        """
        Gets transaction data by transaction hash.
        :param hash: Transaction hash
        :return: Transaction data as dict
        """
        tx = self._rpc.call("getTransactionByHash", hash)
        if tx.get("data") is not None:
            tx["data"] = unhexlify(tx["data"])
        # NOTE: The official client doesn't return raw transaction data
        if tx.get("raw") is not None:
            tx["raw"] = unhexlify(tx["raw"])
        return tx

    # TODO: getTransactionByBlockHashAndIndex,
    #       getTransactionByBlockNumberAndIndex,
    #       getTransactionReceipt

    def mempool(self):
        """
        :return: A list of transactions that are currently in the mempool.
        """
        return self._rpc.call("mempool")

    def mining(self) -> bool:
        """
        :return: True if mining is enabled, False otherwise.
        """
        return self._rpc.call("mining")

    def hashrate(self):
        """
        :return: The current hashrate (in Hash/s), if mining is enabled.
        """
        return self._rpc.call("hashrate")

    def accounts(self):
        """
        :return: Returns a list of accounts. A account is a dict of account_id and address.
        """
        return self._rpc.call("accounts")

    def create_account(self):
        """
        Creates a new account
        :return: The wallet as dict with account_id, address and public_key
        """
        return self._rpc.call("createAccount")

    def get_balance(self, address: str) -> Decimal:
        """
        Returns the balance for an address.
        :param address: The address
        :return: The balance in NIM (as Decimal)
        """
        return satoshi_to_coin(self._rpc.call("getBalance", address))

    def block_number(self):
        """
        :return: The current block chain height.
        """
        return self._rpc.call("blockNumber")

    def get_block_by_hash(self, hash: str, include_txs: bool = False) -> dict:
        """
        Get block by hash
        :param hash: Block hash
        :param include_txs: Whether to include transactions
        :return: The block
        """
        return self._rpc.call("getBlockByHash", hash, include_txs)

    def get_block_by_number(self, number: int, include_txs: bool = False) -> dict:
        """
        Get block by number
        :param hash: Block number
        :param include_txs: Whether to include transactions
        :return: The block
        """
        return self._rpc.call("getBlockByNumber", number, include_txs)
