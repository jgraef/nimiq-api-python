from pprint import pprint

from nimiqrpc import NimiqApi
from nimiqrpc.util import block_listener


nimiq = NimiqApi()

for block in block_listener(nimiq):
    pprint(block)
    print()