from web3.auto import w3
import json

# Read Asset Addresses from .json file
with open("utils/asset_addresses.json", 'r') as jsonfile:
    ASSET_ADDRESSES = json.load(jsonfile)

def get_liquity_event(result, event_name="Liquity_liquidations", return_header=False):
    if event_name == 'Liquity_liquidations':
        
        if return_header:
            return "transactionHash,userLiquidated,blockNumber"
        
        result_dict = {
            'transactionHash' : result["transactionHash"].hex(),
            'borrower' : '0x' + result["topics"][1].hex().lstrip('0x').rjust(40,'0'),
            'blockNumber' : result["blockNumber"],
        }
    else:
        print(f"No event found with name {event_name}")
        return
    return result_dict