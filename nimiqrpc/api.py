__all__ = ["NimiqApi", "ACCOUNT_BASIC", "ACCOUNT_VESTING", "ACCOUNT_HTLC", "TX_NONE", "TX_CONTRACT_CREATION"]

from binascii import hexlify, unhexlify

from decimal import Decimal
from typing import Union

from .jsonrpc import JsonRpcClient
from .util import satoshi_to_coin, ensure_satoshi


ACCOUNT_BASIC = 0
ACCOUNT_VESTING = 1
ACCOUNT_HTLC = 2

TX_NONE = 0
TX_CONTRACT_CREATION = 1


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

    def __init__(self, url="http://localhost:8648", credentials=None):
        """
        :param url: URL to RPC endpoint (default: ``http://localhost:8648``)
        """
        self._rpc = JsonRpcClient(url, credentials)

    def send_raw_transaction(self, tx: bytes):
        """
        Sends a raw transaction
        :param tx: Raw transaction (as bytes)
        :return: Transaction hash (as hex string)
        """
        return self._rpc.call("sendRawTransaction", hexlify(tx).decode())

    def send_transaction(self, from_addr: str, to_addr: str, value: Union[int, Decimal], fee: Union[int, Decimal], to_type: int = ACCOUNT_BASIC, flags: int = TX_NONE, data: bytes = None):
        """
        Sends a transaction
        :param from_addr: Sender address
        :param to_addr: Receiver address
        :param value: Value in Satoshis (int) or NIMs (Decimal)
        :param fee: Fee in Satoshis (int) or NIMs (Decimal)
        :param to_type: Receiver account type (default BASIC)
        :param data: Transaction data needed for extended transactions (bytes)
        :return: Transaction hash
        """
        return self._rpc.call("sendTransaction", {
            "from": from_addr,
            "to": to_addr,
            "value": ensure_satoshi(value),
            "fee": ensure_satoshi(fee),
            "flags": flags,
            "data": None if data is None else hexlify(data).decode(),
            "toType": to_type
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
        return tx

    def mempool(self):
        """
        :return: A list of transactions that are currently in the mempool.
        """
        return self._rpc.call("mempool")

    def mempool_content(self, include_txs=False):
        return self._rpc.call("mempoolContent", include_txs)

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
        :param number: Block number
        :param include_txs: Whether to include transactions
        :return: The block
        """
        return self._rpc.call("getBlockByNumber", number, include_txs)

    def get_block_transaction_count_by_number(self, number: int) -> int:
        return self._rpc.call("getBlockTransactionCountByNumber", number)

    def get_block_transaction_count_by_hash(self, hash: str) -> int:
        return self._rpc.call("getBlockTransactionCountByHash", hash)

    def get_transaction_by_block_hash_and_index(self, hash: str, index: int) -> dict:
        return self._rpc.call("getTransactionByBlockHashAndIndex", hash, index)

    def get_transaction_by_block_number_and_index(self, number: int, index: int) -> dict:
        return self._rpc.call("getTransactionByBlockNumberAndIndex", number, index)

    def get_transaction_receipt(self, hash: str) -> dict:
        return self._rpc.call("getTransactionReceipt", hash)

    def get_transactions_by_address(self, address: str, limit: int = None):
        return self._rpc.call("getTransactionsByAddress", address, limit)

    def peer_count(self):
        return self._rpc.call("peerCount")

    def peer_list(self):
        return self._rpc.call("peerList")

    def peer_state(self, peer, state = None):
        return self._rpc.call("peerState", peer, state)

    def consensus(self):
        return self._rpc.call("consensus")

    def import_raw_key(self, key_data, password=""):
        return self._rpc.call("importRawKey", hexlify(key_data).decode(), password)

    def lock_account(self, address):
        return self._rpc.call("lockAccount", address)

    def unlock_account(self, address, password=""):
        return self._rpc.call("unlockAccount", address, password)
