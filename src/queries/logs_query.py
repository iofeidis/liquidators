from web3.auto import w3
import csv
import json
from events.event_specifics import get_event_values
import pandas as pd


def run_query(filepath: str="results/test.csv",
              start_block: int=1500000,
              end_block: int=15940000,
              event_name: str="Maker_v1_Bite"):
    
    # Read Event Signatures from .json file
    with open("utils/event_signatures.json", 'r') as jsonfile:
        all_signatures = json.load(jsonfile)
    event_signature = w3.keccak(text=all_signatures[event_name]).hex()
    # event_signature = w3.keccak(text=event_name).hex()
    
    with open(filepath, 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        header = get_event_values(None, event_name, return_header=True)
        spamwriter.writerow(header.split(','))

        # Scrape 8,000 blocks per request
        for p, i in enumerate(range(start_block, end_block, 8000)):
        
            params = {'fromBlock': i,
                    'toBlock': min(end_block, i + 8000),
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
                result_dict = get_event_values(result, event_name)
                spamwriter.writerow(result_dict.values())
                
    if  event_name == 'Maker_v1_Bite' or \
        event_name == 'Maker_v2_Bark' or \
        event_name == 'Liquity_liquidations':
            
        # Add liquidators for each transaction
        df = pd.read_csv(filepath)
        l = [w3.eth.get_transaction(i)['from'] for i in df.transactionHash.values]
        df.insert(loc=1, column='liquidator', value=l)
        df.to_csv(filepath, index=False)
