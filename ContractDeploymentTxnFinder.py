import argparse
import pprint
import sys
from web3 import Web3, HTTPProvider

parser = argparse.ArgumentParser()
parser.add_argument("address", help="represents contract address")
parser.add_argument("--host", help="Network where contract is deployed")
args = parser.parse_args()
w3 = Web3(Web3.HTTPProvider(args.host))
contract_address     = w3.toChecksumAddress(args.address)

def handle_event(event):
    #pprint.pprint(event)
    eventdict = dict(event[0])
    if 'blockHash' in eventdict:
        print("BlockHash : {}".format(eventdict['blockHash'].hex()))
    if 'transactionHash' in eventdict:
        print("TransactionHash : {}".format(eventdict['transactionHash'].hex()))


def log(event):
    #for event in event_filter.get_all_entries():
    handle_event(event)

if __name__ == "__main__":

    event_signature_hash = w3.sha3(text="ContractDeployed(string)").hex()
    contract_deployed_event_filter = w3.eth.getLogs({
        "fromBlock": 0,
        "from": contract_address,
        "topics": [event_signature_hash],
        })
    log(contract_deployed_event_filter)
