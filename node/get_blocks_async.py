from web3.auto import w3
import time
import asyncio
from web3 import Web3, AsyncHTTPProvider
from web3.eth import AsyncEth
from web3.net import AsyncNet

START_BLOCK = 14000000
END_BLOCK = 14010000

print(f"Node is connected: {w3.isConnected()}")

rpc_node_url = 'http://localhost:8545'
w3_async = Web3(AsyncHTTPProvider(rpc_node_url), modules={'eth': (AsyncEth,), 'net': (AsyncNet,)}, middlewares=[])


async def get_block(block_number):
    return await w3_async.eth.get_block(block_number)

async def main():
    # start_time = time.time()
    tasks = [get_block(x) for x in range(START_BLOCK, END_BLOCK)]
    task_results = await asyncio.gather(*tasks, return_exceptions=True)
    print(len(task_results))
    # end_time = time.time()
    # print(end_time - start_time)
    
asyncio.run(main())
