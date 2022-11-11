from web3.auto import w3
import json

# Read Asset Addresses from .json file
with open("utils/asset_addresses.json", 'r') as jsonfile:
    ASSET_ADDRESSES = json.load(jsonfile)

def get_maker_event(result, event_name):
    if event_name == 'Maker_v1_Bite':
        
        # HEADER = "transactionHash,userLiquidated,collateralAsset," + \
        # "debtToCover,blockNumber,liquidator"
        
        
        result_dict = {
            'transactionHash' : result["transactionHash"].hex(),
            'vault_address' : '0x' + result["topics"][2].hex().lstrip('0x').rjust(40,'0'),
            'collateralAsset' : w3.toText(result["topics"][1]).rstrip('\x00'),
            'debt_dai': round(int(result["data"][130:130+64], base=16) / 10**45, 3),
            'blockNumber' : result["blockNumber"],
        }

    elif event_name == 'Maker_v2_Bark':
        
        # HEADER = "transactionHash,userLiquidated,collateralAsset," + \
        # "debtToCover,blockNumber,liquidator"
        
        
        result_dict = {
            'transactionHash' : result["transactionHash"].hex(),
            'vault_address' : '0x' + result["topics"][2].hex().lstrip('0x').rjust(40,'0'),
            'collateralAsset' : w3.toText(result["topics"][1]).rstrip('\x00'),
            'debt_dai': round(int(result["data"][66:130], base=16) / 10**18, 3),
            'blockNumber' : result["blockNumber"],
        }

    else:
        print(f"No event found with name {event_name}")
        return
    return result_dict