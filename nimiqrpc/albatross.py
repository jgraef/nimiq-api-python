from binascii import hexlify, unhexlify

from decimal import Decimal
from typing import Union

from .api import NimiqApi, ensure_satoshi


ACCOUNT_STAKING = 3

# Address of Staking Contract in DevNet
STAKING_CONTRACT_ADDRESS = "NQ60 GA6V BV8S YVX1 XGCY 88LR D2K6 G2P4 U9MH"


class AlbatrossApi(NimiqApi):
    def validator_key(self):
        ret = self._rpc.call("validatorKey")
        return {
            "validator_key": unhexlify(ret["validatorKey"]),
            "proof_of_knowledge": unhexlify(ret["proofOfKnowledge"])
        }

    def stake(self, reward_address: str, staker_address: str, value: Union[int, Decimal]):
        validator_info = self.validator_key()
        self._rpc.call(
            "stake",
            hexlify(validator_info["validator_key"]).decode(),
            hexlify(validator_info["proof_of_knowledge"]).decode(),
            staker_address,
            ensure_satoshi(value),
            reward_address
        )
