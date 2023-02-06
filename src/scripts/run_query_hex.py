from web3.auto import w3
import csv
import json
import pandas as pd

print(f"Node is connected : {w3.isConnected()}")

START_BLOCK = 15000000
# Check what JSON-RPC thinks as the latest block number
END_BLOCK = 16000000
FILE = "results/test.csv"
HEADER = "transactionHash,initiator,asset,amount,blockNumber"

# EVENT_NAME = 'Kick(uint256,uint256,uint256,uint256,address,address,uint256)'
# EVENT_NAME = 'Take(uint256,uint256,uint256,uint256,uint256,uint256,address)'
# EVENT_NAME = 'Kick(uint256,uint256,uint256,uint256,address,address)'
# EVENT_NAME = 'LogNote(bytes4,address,bytes32,bytes32,bytes)'
# EVENT_NAME = 'LogTrade(uint,address,uint,address)'
# EVENT_NAME = 'Bite(bytes32,address,uint256,uint256,uint256,address,uint256)'
# EVENT_NAME = 'FlashLoan(address,address,address,uint256,uint8,uint256,uint16)' #aave v3 flashloan
# EVENT_NAME = 'FlashLoan(address,address,address,uint256,uint256,uint16)'
# EVENT_NAME = 'RepayBorrow(address,address,uint256,uint256,uint256)'
# EVENT_NAME = 'FlashLoan(address,address,address,uint256,bytes8,uint256,uint16)'
EVENT_NAME = 'Mint(address,uint256,uint256)'

if __name__=="__main__":
    """
    Script to query and print a specific event signature
    not in the currently provided ones
    Does not save anything in .csv files!
    """
    

    event_signature = w3.keccak(text=EVENT_NAME).hex()
    
    with open(FILE, 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(HEADER.split(','))

        # Scrape 8,000 blocks per request
        for p, i in enumerate(range(START_BLOCK, END_BLOCK, 1000)):
        
            params = {'fromBlock': i,
                    'toBlock': min(END_BLOCK, i + 1000),
                    'topics': [
                        [event_signature],]
                    }

            # Query based on Logs
            results = w3.eth.get_logs(params)
            if p % 50 == 0:
                print(f"Querying Block: {i}")

            for result in results:
                print(result)
                exit()