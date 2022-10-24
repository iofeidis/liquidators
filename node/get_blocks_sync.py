from web3.auto import w3


START_BLOCK = 14000000
END_BLOCK = 14010000

print(f"Node is connected: {w3.isConnected()}")

for i in range(START_BLOCK, END_BLOCK):
    # if i % 100 == 0:
    #     print(f"Current Block: {i}")
    block = w3.eth.get_block(i)
