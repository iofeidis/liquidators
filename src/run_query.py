from web3.auto import w3
import csv
import json
from event_specifics import get_event_values

print(f"Node is connected : {w3.isConnected()}")

START_BLOCK = 14000000
# Check what JSON-RPC thinks as the latest block number
END_BLOCK = 15050000
FILE = "results/node.csv"
HEADER = "transactionHash,userLiquidated,collateralAsset,debtAsset," + \
        "liquidator,debtToCover,liquidatedCollateralAmount,blockNumber"
EVENT_NAME = 'Kick(uint256,uint256,uint256,uint256,address,address,uint256)'

if __name__=="__main__":

    # Read Event Signatures from .json file
    with open("utils/event_signatures.json", 'r') as jsonfile:
        all_signatures = json.load(jsonfile)
    # event_signature = w3.keccak(text=all_signatures[EVENT_NAME]).hex()
    event_signature = w3.keccak(text=EVENT_NAME).hex()
    
    with open(FILE, 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(HEADER.split(','))

        # Scrape 8,000 blocks per request
        for p, i in enumerate(range(START_BLOCK, END_BLOCK, 8000)):
        
            params = {'fromBlock': i,
                    'toBlock': min(END_BLOCK, i + 8000),
                    'topics': [
                        [event_signature],]
                    }

            results = w3.eth.get_logs(params)
            if p % 50 == 0:
                print(f"Querying Block: {i}")

            for result in results:
                print(result)
                exit()
                result_dict = get_event_values(result, EVENT_NAME)
                spamwriter.writerow(result_dict.values())