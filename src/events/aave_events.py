from web3.auto import w3
import json

# Read Asset Addresses from .json file
with open("utils/asset_addresses.json", 'r') as jsonfile:
    ASSET_ADDRESSES = json.load(jsonfile)

def get_aave_event(result, event_name):
    # Same as Aave v2 liquidations
    if event_name == 'Aave_v3_liquidations':
        
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
    elif event_name == 'Aave_v1_liquidations':
        
        collateral_asset = '0x' + result["topics"][1].hex().lstrip('0x').rjust(40,'0')
        debt_asset = '0x' + result["topics"][2].hex().lstrip('0x').rjust(40,'0')
        
        result_dict = {
            'transactionHash' : result["transactionHash"].hex(),
            'userLiquidated' : '0x' + result["topics"][3].hex().lstrip('0x').rjust(40,'0'),
            'collateralAsset' : ASSET_ADDRESSES[collateral_asset],
            'debtAsset' : ASSET_ADDRESSES[debt_asset],
            'liquidator' : '0x' + result["data"][218:258],
            'debtToCover' : int(result["data"][0:66], base=16),
            'liquidatedCollateralAmount' : int(result["data"][66:130], base=16),
            'blockNumber' : result["blockNumber"],
        }
    else:
        print(f"No event found with name {event_name}")
        return
    return result_dict