import argparse
import pprint
import sys
from web3 import Web3, HTTPProvider
import web3

parser = argparse.ArgumentParser()
parser.add_argument("address", help="represents contract address")
parser.add_argument("--host", help="Network where contract is deployed")
args = parser.parse_args()
w3 = Web3(Web3.HTTPProvider(args.host, request_kwargs={'timeout': 1200}))
contract_address = w3.toChecksumAddress(args.address)

def searchTransactionsByBlock(startBlockNumber , endBlockNumber):
    for i in range(startBlockNumber, endBlockNumber+1):
        print(i)
        block = w3.eth.getBlock(i)
        if len(dict(block)['transactions']) > 0:
            for txn in dict(block)['transactions']:
                txndict = dict(w3.eth.getTransaction(txn))
                if 'to' in txndict and ( txndict['to'] == '0x0' ):
                        #pprint.pprint(txndict)
                        receiptdict = dict(w3.eth.getTransactionReceipt(txn))
                        #pprint.pprint(receiptdict)
                        if receiptdict['contractAddress'] == contract_address:
                            #print("New Contract : {}".format(receiptdict['contractAddress']))
                            print("BlockHash : {}".format(receiptdict['blockHash'].hex()))
                            print("TransactionHash : {}".format(receiptdict['transactionHash'].hex()))
                            return

if __name__ == "__main__":
    print(contract_address)
    print(w3.eth.blockNumber)
    searchTransactionsByBlock(0, w3.eth.blockNumber)
