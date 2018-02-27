from nimiqrpc import NimiqApi


nimiq = NimiqApi()

for account in nimiq.accounts():
    balance = nimiq.get_balance(account["address"])
    print("{!s}: {!s} NIM".format(account["address"], balance))
