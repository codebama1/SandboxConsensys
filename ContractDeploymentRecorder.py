import argparse
import pprint
import sys
import time
import asyncio
from web3 import Web3, HTTPProvider

parser = argparse.ArgumentParser()
parser.add_argument("--host", help="Network where contract is deployed")
args = parser.parse_args()
w3 = Web3(Web3.HTTPProvider(args.host, request_kwargs={'timeout': 60}))
contract_deployed_list = []


def handle_event(txn):
    pprint.pprint(txn)
    txndict = dict(w3.eth.getTransaction(txn))
    if 'to' in txndict and ( txndict['to'] == '0x0' ):
            pprint.pprint(txndict)
            receiptdict = dict(w3.eth.getTransactionReceipt(txn))
            pprint.pprint(receiptdict)
            if 'contractAddress' in receiptdict:
                print("New Contract : {}".format(receiptdict['contractAddress']))
                print("BlockHash : {}".format(receiptdict['blockHash'].hex()))
                print("TransactionHash : {}".format(receiptdict['transactionHash'].hex()))
                contract_dict = {"contractAddress" : receiptdict['contractAddress'], "host" : args.host, "blockHash" : receiptdict['blockHash'].hex(), "transactionHash" : receiptdict['transactionHash'].hex()}
                contract_deployed_list.append(contract_dict)


async def log_loop(txn_filter, poll_interval):
    while True:
        for txn in txn_filter.get_new_entries():
            handle_event(txn)
        await asyncio.sleep(poll_interval)

def main():
    tx_filter = w3.eth.filter('pending')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(log_loop(tx_filter, 2)))
    finally:
        loop.close()


if __name__ == '__main__':
    main()
