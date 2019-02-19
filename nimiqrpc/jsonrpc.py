__all__ = ["JsonRpcError", "JsonRpcRemoteException", "JsonRpcClient"]

from itertools import count
import logging

import requests


logger = logging.getLogger(__name__)


class JsonRpcError(Exception):
    """ Internal error during a JSON RPC request. """
    pass


class JsonRpcRemoteException(Exception):
    """ Exception on the remote server """
    def __init__(self, req, resp):
        self.request = req
        self.response = resp
        super(JsonRpcRemoteException, self).__init__("Remote Error: {!s}".format(resp["error"]))


class JsonRpcClient:
    """ A very minimal JSON RPC client """

    def __init__(self, url, credentials=None):
        """
        Creates a JSON RPC client
        :param url: The URL to the API endpoint
        """
        self.url = url
        self.credentials = credentials
        self.session = requests.Session()
        self.call_ids = count(1)

    def call(self, method, *args):
        """
        Calls a remote procedure

        :param method: Method name
        :param args: Argument list
        :return: The result of the remote procedure

        NOTE: Since the Nimiq JSON RPC server only supports positional arguments, we don't care about keyword arguments.
        """

        call_id = next(self.call_ids)
        rpc_req = {
            "jsonrpc": "2.0",
            "method": method,
            "params": args,
            "id": call_id
        }
        logger.info("Request: {!r}".format(rpc_req))

        resp = requests.post(
            self.url,
            json=rpc_req,
            auth=self.credentials
        )
        resp.raise_for_status()

        rpc_resp = resp.json()
        logger.info("Response (call_id={:d}): {!r}".format(call_id, rpc_resp))
        if rpc_resp.get("id") != call_id:
            raise JsonRpcError("Response with incorrect call ID. Expected {:d}, but received {!s}".format(call_id, rpc_resp.get("id")))

        result = rpc_resp.get("result")
        error = rpc_resp.get("error")
        if error is not None:
            raise JsonRpcRemoteException(rpc_req, rpc_resp)
        return result
