from web3.auto import w3
import csv

print(f"Node is connected : {w3.isConnected()}")

START_BLOCK = 14000000
# Check what JSON-RPC thinks as the latest block number
END_BLOCK = 14000300
FILE = "tx.csv"
HEADER = "from,to,value,blockNumber,hash"

if __name__=="__main__":

    with open(FILE, 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(HEADER.split(','))

        for i in range(START_BLOCK, END_BLOCK):
            if i % 100 == 0:
                print(f"Current Block: {i}")
            # Get the number of transactions in this block
            a = len(w3.eth.get_block(i).transactions)
            for j in range(a):
                # Get a specific transaction in this block
                tx = w3.eth.get_transaction_by_block(i, j)
                spamwriter.writerow([tx['from'], tx['to'], tx['value'],
                                     tx['blockNumber'], tx['hash'].hex( )])