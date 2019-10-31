from pprint import pprint

from nimiqrpc import NimiqApi
from nimiqrpc.util import block_listener


nimiq = NimiqApi()

for block in block_listener(nimiq):
    txs = []
    for txid in block["transactions"]:
        txs.append(nimiq.get_transaction_by_hash(txid))
    block["transactions"] = txs
    pprint(block)
    print()
