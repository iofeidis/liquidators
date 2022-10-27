from web3.auto import w3
import csv
import json
from event_specifics import get_event_values
import pandas as pd

print(f"Node is connected : {w3.isConnected()}")

START_BLOCK = 11000000
# Check what JSON-RPC thinks as the latest block number
END_BLOCK = 15800000
FILE = "results/compound_v2_liquidations.csv"
# HEADER = "transactionHash,initiator,asset,amount,blockNumber"
HEADER = "transactionHash,userLiquidated,collateralAsset," + \
        "liquidator,debtToCover,liquidatedCollateralAmount,blockNumber"

# EVENT_NAME = 'Aave_v3_liquidations'
# EVENT_NAME = 'Aave_v2_flashloans'
EVENT_NAME = 'Compound_v2_liquidations'

# EVENT_NAME = 'Kick(uint256,uint256,uint256,uint256,address,address,uint256)'
# EVENT_NAME = 'Take(uint256,uint256,uint256,uint256,uint256,uint256,address)'
# EVENT_NAME = 'Kick(uint256,uint256,uint256,uint256,address,address)'
# EVENT_NAME = 'LogNote(bytes4,address,bytes32,bytes32,bytes)'
# EVENT_NAME = 'LogTrade(uint,address,uint,address)'
# EVENT_NAME = 'Bite(bytes32,address,uint256,uint256,uint256,address,uint256)'
# EVENT_NAME = 'LiquidateBorrow(address,address,uint256,address,uint256)'
# EVENT_NAME = 'BorrowLiquidated(address,address,uint256,uint256,uint256,uint256,address,address,uint256,uint256,uint256,uint256)'
# EVENT_NAME = 'SupplyReceived(address,address,uint256,uint256,uint256)'

if __name__=="__main__":

    # Read Event Signatures from .json file
    with open("utils/event_signatures.json", 'r') as jsonfile:
        all_signatures = json.load(jsonfile)
    event_signature = w3.keccak(text=all_signatures[EVENT_NAME]).hex()
    # event_signature = w3.keccak(text=EVENT_NAME).hex()
    
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

            # Query based on Logs
            results = w3.eth.get_logs(params)
            if p % 50 == 0:
                print(f"Querying Block: {i}")

            for result in results:
                # print(result)
                # exit()
                result_dict = get_event_values(result, EVENT_NAME)
                spamwriter.writerow(result_dict.values())
                
    if EVENT_NAME == 'Maker_v1_Bite':
        # Add liquidators for each transaction
        df = pd.read_csv(FILE)
        l = [w3.eth.get_transaction(i)['from'] for i in df.transactionHash.values]
        df['liquidator'] = pd.DataFrame(l)
        df.to_csv(FILE)