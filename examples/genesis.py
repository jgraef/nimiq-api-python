from pprint import pprint

from nimiqrpc import NimiqApi


nimiq = NimiqApi()
pprint(nimiq.get_block_by_number(1))
