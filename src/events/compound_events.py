from web3.auto import w3
import json

# Read Asset Addresses from .json file
with open("utils/asset_addresses.json", 'r') as jsonfile:
    ASSET_ADDRESSES = json.load(jsonfile)

def get_compound_event(result, event_name):
    if event_name == 'Compound_v1_liquidations':
        
        # HEADER = "transactionHash,userLiquidated,collateralAsset,debtAsset," + \
        # "liquidator,debtToCover,liquidatedCollateralAmount,blockNumber"
        
        collateral_asset = '0x' + result["data"][474:514]
        debt_asset = '0x' + result["data"][90:130]
        
        result_dict = {
            'transactionHash' : result["transactionHash"].hex(),
            'userLiquidated' : '0x' + result["data"][26:66],
            'collateralAsset' : ASSET_ADDRESSES[collateral_asset] if collateral_asset in ASSET_ADDRESSES.keys() else collateral_asset,
            'debtAsset' : ASSET_ADDRESSES[debt_asset] if debt_asset in ASSET_ADDRESSES.keys() else debt_asset,
            'liquidator' : '0x' + result["data"][410:450],
            'debtToCover' : int(result["data"][260:322], base=16),
            'liquidatedCollateralAmount' : int(result["data"][643:706], base=16),
            'blockNumber' : result["blockNumber"],
        }
    elif event_name == 'Compound_v2_liquidations':
        
        # HEADER = "transactionHash,userLiquidated,collateralAsset," + \
        # "liquidator,debtToCover,liquidatedCollateralAmount,blockNumber"
        
        collateral_asset = '0x' + result["data"][218:258]
        
        result_dict = {
            'transactionHash' : result["transactionHash"].hex(),
            'userLiquidated' : '0x' + result["data"][90:130],
            'collateralAsset' : ASSET_ADDRESSES[collateral_asset] if collateral_asset in ASSET_ADDRESSES.keys() else collateral_asset,
            'liquidator' : '0x' + result["data"][26:66],
            'debtToCover' : int(result["data"][130:194], base=16),
            'liquidatedCollateralAmount' : int(result["data"][270:322], base=16),
            'blockNumber' : result["blockNumber"],
        }
    else:
        print(f"No event found with name {event_name}")
        return
    return result_dict