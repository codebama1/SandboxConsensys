import argparse
import pprint
import sys
import asyncio
from web3 import Web3, HTTPProvider
import web3
import logging
from threading import Thread
import concurrent.futures

parser = argparse.ArgumentParser()
parser.add_argument("address", help="represents contract address")
parser.add_argument("--host", help="Network where contract is deployed")
args = parser.parse_args()
w3 = Web3(Web3.HTTPProvider(args.host, request_kwargs={'timeout': 1200}))
contract_address = w3.toChecksumAddress(args.address)

def searchTransactionsByBlock(startBlockNumber , endBlockNumber):
    totalBlocks = w3.eth.blockNumber
    if startBlockNumber > totalBlocks:
        return 0
    elif endBlockNumber > totalBlocks:
        endBlockNumber = totalBlocks
    for i in range(startBlockNumber, endBlockNumber+1):
        print(i)
        #await asyncio.sleep(1)
        block = w3.eth.getBlock(i)
        if len(dict(block)['transactions']) > 0:
            for txn in dict(block)['transactions']:
                txndict = dict(w3.eth.getTransaction(txn))
                if 'to' in txndict and ( txndict['to'] == '0x0' ):
                        #pprint.pprint(txndict)
                        receiptdict = dict(w3.eth.getTransactionReceipt(txn))
                        #pprint.pprint(receiptdict)
                        if receiptdict['contractAddress'] == contract_address:
                            print("New Contract : {}".format(receiptdict['contractAddress']))
                            print("BlockHash : {}".format(receiptdict['blockHash'].hex()))
                            print("TransactionHash : {}".format(receiptdict['transactionHash'].hex()))
                            asyncio.get_event_loop().close()
                            sys.exit(1)
                            #return 1
    return 0


async def run_tasks_parallely(executor, threadCount):
    log = logging.getLogger('run_tasks_parallely')
    log.info('starting')

    log.info('creating executor tasks')
    loop = asyncio.get_event_loop()
    blocking_tasks = [
        loop.run_in_executor(executor, searchTransactionsByBlock, (i*1000)+1, (i*1000)+1000)
        for i in range(threadCount+1)
    ]
    log.info('waiting for executor tasks')
    #log.info('waiting for executor tasks')
    completed,pending = await asyncio.wait(blocking_tasks)
    results = [t.result() for t in completed]
    log.info('results: {!r}'.format(results))
    #for result in results:
        #if (result == 1):
            #loop.close()
            #sys.exit(1)
    log.info('exiting')



if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        #filename='./async.log',
        format='%(threadName)10s %(name)18s: %(message)s',
        stream=sys.stderr,
    )
    #Print basic info
    print(contract_address)
    print(w3.eth.blockNumber)
    threadCount = int(w3.eth.blockNumber/1000)

    # Create a limited thread pool.
    executor = concurrent.futures.ThreadPoolExecutor(
        max_workers=threadCount,
    )

    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(run_tasks_parallely(executor, threadCount))
