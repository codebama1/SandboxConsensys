import argparse
import pprint
import sys
from web3 import Web3, HTTPProvider
import ContractDeploymentRecorder

parser = argparse.ArgumentParser()
parser.add_argument("address", help="This is contract address")
parser.add_argument("--host", help="Network where contract is deployed")
args = parser.parse_args()
w3 = Web3(Web3.HTTPProvider(args.host, request_kwargs={'timeout': 60}))
contract_address     = w3.toChecksumAddress(args.address)
contract_deployed_list = [] #Get from ContractDeploymentRecorder list

def find():
    for contract in contract_deployed_list:
        contractdict = dict(contract)
        if contractdict['contractAddress'] == contract_address and contractdict['host'] == args.host:
            print("New Contract : {}".format(contractdict['contractAddress']))
            print("BlockHash : {}".format(contractdict['blockHash'].hex()))
            print("TransactionHash : {}".format(contractdict['transactionHash'].hex()))

if __name__ == '__main__':
    find()
