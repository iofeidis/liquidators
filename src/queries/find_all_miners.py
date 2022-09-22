from web3.auto import w3
import csv

print(f"Node is connected : {w3.isConnected()}")

START_BLOCK = 0
# Check what JSON-RPC thinks as the latest block number
END_BLOCK = 15095000
FILE = "results/miners.csv"
HEADER = "miner_address,block_mined"

if __name__=="__main__":

    with open(FILE, 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(HEADER.split(','))

        for i in range(START_BLOCK, END_BLOCK):
            if i % 1000000 == 0:
                print(f"Current Block: {i}")
            # Get the number of transactions in this block
            miner_address = w3.eth.get_block(i).miner
            spamwriter.writerow([miner_address,i])