from sys import stdout, argv

from pprintpp import pprint

from nimiqrpc.albatross import *
from nimiqrpc.util import block_listener


try:
    rpc_url = argv[1]
except IndexError:
    rpc_url = None

try:
    rpc_credentials = argv[2:3]
except IndexError:
    rpc_credentials = None


nimiq = AlbatrossApi(rpc_url, rpc_credentials)


for block in block_listener(nimiq):
    if block["type"] == "macro":
        print()
        pprint(block)
        print()
        print()
    else:
        print(".", end="")
        stdout.flush()

