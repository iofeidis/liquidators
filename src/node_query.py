from web3.auto import w3
import csv
import json

print(f"Node is connected : {w3.isConnected()}")

START_BLOCK = 15050000
END_BLOCK = 15057000
FILE = "results/node.csv"
HEADER = "transactionHash,userLiquidated,collateralAsset,debtAsset," + \
        "liquidator,debtToCover,liquidatedCollateralAmount,blockNumber"

# Read Asset Addresses from .json file
with open("utils/asset_addresses.json", 'r') as jsonfile:
    ASSET_ADDRESSES = json.load(jsonfile)

# Read Event Signatures from .json file
with open("utils/event_signatures.json", 'r') as jsonfile:
    EVENT_SIGNATURES = json.load(jsonfile)

EVENT_SIGNATURE = EVENT_SIGNATURES['Aave_v3_liquidations']
event_signature = w3.keccak(text=EVENT_SIGNATURE).hex()

## This is Event Signature specific
def get_result(result):
    collateral_asset = '0x' + result["topics"][1].hex().lstrip('0x').rjust(40,'0')
    debt_asset = '0x' + result["topics"][2].hex().lstrip('0x').rjust(40,'0')
    
    result_dict = {
                'transactionHash' : result["transactionHash"].hex(),
                'userLiquidated' : '0x' + result["topics"][3].hex().lstrip('0x').rjust(40,'0'),
                'collateralAsset' : ASSET_ADDRESSES[collateral_asset],
                'debtAsset' : ASSET_ADDRESSES[debt_asset],
                'liquidator' : '0x' + result["data"][154:194],
                'debtToCover' : int(result["data"][:66], base=16),
                'liquidatedCollateralAmount' : int(result["data"][66:130], base=16),
                'blockNumber' : result["blockNumber"],
            }
    return result_dict

if __name__=="__main__":
    with open(FILE, 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(HEADER.split(','))

        for i in range(START_BLOCK, END_BLOCK, 8000):
        
            params = {'fromBlock': i,
                    'toBlock': min(END_BLOCK, i + 8000),
                    'topics': [
                        [event_signature],]
                    }

            results = w3.eth.get_logs(params)
            if i % 1000000 == 0:
                print(f"Querying Block: {i}")

            for result in results:
                result_dict = get_result(result)
                spamwriter.writerow(result_dict.values())