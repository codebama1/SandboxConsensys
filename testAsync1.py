import asyncio
import concurrent.futures
import logging
import sys
import time

def target(loop, x, y, timeout=None):
    log = logging.getLogger('run_tasks_parallelly')
    log.info('starting')
    #futures = []
    #for i in range(7):
    future = asyncio.run_coroutine_threadsafe(add(x, b=y), loop)
    #future[i].result(timeout)
    log.info('finished')
    return future.result(timeout)
    #return future

def targetController(loop):
    for i in range(7):
        res = target(loop, i, i+1)
        print(res)
        if res == 9:
            return res
    return 0


async def add(a, b):
    await asyncio.sleep(1)
    return a + b

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        #filename='./async.log',
        format='%(threadName)10s %(name)18s: %(message)s',
        stream=sys.stderr,
    )
    loop = asyncio.get_event_loop()
    #for i in range(7):
            #log = logging.getLogger('run_tasks_parallelly')
            #log.info('starting')
            #future = asyncio.run_coroutine_threadsafe(add(i, b=i+1), loop)
            #log.info('finished')
            #result = future.result(None)
            #print(result)
            #if result == 9:
                #loop.close()
                #break
                #sys.exit(1)
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=3,)
    future = loop.run_in_executor(executor, targetController, loop)
    #for i in range(7):
        #future = loop.run_in_executor(executor, target, loop, i, i+1)
        #results = []
        #for future in futures:
            #print(future.result())
            #results.append(future.result())
        #results = [t.result() for t in future]
        #log.info('results: {!r}'.format(results))
    result = loop.run_until_complete(future)
    print(loop.run_until_complete(future))
    if result == 9:
        loop.close()
            #break
        sys.exit(1)
        #assert loop.run_until_complete(future) == 3
