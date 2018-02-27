import code
from functools import partial

from nimiqrpc import NimiqApi


BANNER = """
Nimiq JSON-API Python Shell

Type help() for help.
Type exit() or press Ctrl-D to exit.
"""

HELP = """
This interactive python shell exposes the Nimiq RPC methods:

{method_help}

Examples:

   >>> get_block_by_number(0)
   {{'accountsHash': 'c5ec6638e93eda82c1221c24083f9c6b0d85b227c1d14ead5e595eb3c4f272db',
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
    'transactions': []}}

   >>> accounts()
   [{{'id': 'f1ac032bfe0814331d2a57ce74f346c6c75b4eb6', 'address': 'NQ76 X6N0 6AYX 10A3 679A AY77 9US6 QT3M NKMN'}},
    {{'id': '8629c69a857f715aff9a6e5b084eaa15af7730b2', 'address': 'NQ53 GQLU D6L5 FVQM MYUS DRDG GKMA 2NPP EC5J'}}]

   >>> get_balance("NQ53 GQLU D6L5 FVQM MYUS DRDG GKMA 2NPP EC5J")
   Decimal('83503.27457')

   >>> send_transaction("NQ53 GQLU D6L5 FVQM MYUS DRDG GKMA 2NPP EC5J", \
                              "NQ76 X6N0 6AYX 10A3 679A AY77 9US6 QT3M NKMN", \
                               100000, 10)
   '74cee0799277e9f58bf558329ac64bb75ef432e6ca685e4d8986517204a148cf'
 
"""


def shell():
    nimiq = NimiqApi()
    methods = {k: getattr(nimiq, k) for k in dir(nimiq) if not k.startswith("_")}
    METHOD_HELP = "".join(["{!s}:\n{!s}\n\n".format(name, method.__doc__.strip()) for name, method in methods.items()])

    local = dict(
        _nimiq=nimiq,
        help=partial(print, HELP.format(method_help = METHOD_HELP))
    )
    local.update(methods)
    code.interact(BANNER, local=local)


if __name__ == "__main__":
    shell()
