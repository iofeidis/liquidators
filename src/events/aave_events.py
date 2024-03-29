from web3.auto import w3
import json

# Read Asset Addresses from .json file
with open("utils/asset_addresses.json", 'r') as jsonfile:
    ASSET_ADDRESSES = json.load(jsonfile)

def get_aave_event(result=None, event_name="Aave_v1_liquidations", return_header=False):
    # Same as Aave v2 liquidations
    if event_name == 'Aave_v3_liquidations':
        
        if return_header:
            return "transactionHash,userLiquidated,collateralAsset,debtAsset," + \
                "liquidator,debtToCover,liquidatedCollateralAmount,blockNumber"
        
        collateral_asset = '0x' + result["topics"][1].hex().lstrip('0x').rjust(40,'0')
        debt_asset = '0x' + result["topics"][2].hex().lstrip('0x').rjust(40,'0')
        
        result_dict = {
            'transactionHash' : result["transactionHash"].hex(),
            'userLiquidated' : '0x' + result["topics"][3].hex().lstrip('0x').rjust(40,'0'),
            'collateralAsset' : ASSET_ADDRESSES[collateral_asset] if collateral_asset in ASSET_ADDRESSES.keys() else collateral_asset,
            'debtAsset' : ASSET_ADDRESSES[debt_asset] if debt_asset in ASSET_ADDRESSES.keys() else debt_asset,
            'liquidator' : '0x' + result["data"][154:194],
            'debtToCover' : int(result["data"][:66], base=16),
            'liquidatedCollateralAmount' : int(result["data"][66:130], base=16),
            'blockNumber' : result["blockNumber"],
        }
    elif event_name == 'Aave_v1_liquidations':
        
        if return_header:
            return "transactionHash,userLiquidated,collateralAsset,debtAsset," + \
                "liquidator,debtToCover,liquidatedCollateralAmount,blockNumber"
        
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
    elif event_name == 'Aave_v2_flashloans':
        
        if return_header:
            return "transactionHash,initiator,asset,amount,blockNumber"
        
        asset = '0x' + result["topics"][3].hex().lstrip('0x').rjust(40,'0')
        
        result_dict = {
            'transactionHash' : result["transactionHash"].hex(),
            'initiator': '0x' + result["topics"][2].hex().lstrip('0x').rjust(40,'0'),
            'asset': ASSET_ADDRESSES[asset] if asset in ASSET_ADDRESSES.keys() else asset,
            'amount': int(result["data"][0:66], base=16),
            'blockNumber': result["blockNumber"],
        }
    elif event_name == 'Aave_v1_deposits':
        
        if return_header:
            return "transactionHash,depositor,asset,amount,blockNumber"
        
        asset = '0x' + result["topics"][1].hex().lstrip('0x').rjust(40,'0')
        
        result_dict = {
            'transactionHash' : result["transactionHash"].hex(),
            'depositor': '0x' + result["topics"][2].hex().lstrip('0x').rjust(40,'0'),
            'asset': ASSET_ADDRESSES[asset] if asset in ASSET_ADDRESSES.keys() else asset,
            'amount': int(result["data"][0:66], base=16),
            'blockNumber': result["blockNumber"],
        }
    elif event_name == 'Aave_v2_deposits':
        
        if return_header:
            return "transactionHash,depositor,asset,amount,blockNumber"
        
        asset = '0x' + result["topics"][1].hex().lstrip('0x').rjust(40,'0')
        
        result_dict = {
            'transactionHash' : result["transactionHash"].hex(),
            'depositor': '0x' + result["topics"][2].hex().lstrip('0x').rjust(40,'0'),
            'asset': ASSET_ADDRESSES[asset] if asset in ASSET_ADDRESSES.keys() else asset,
            'amount': int(result["data"][67:], base=16),
            'blockNumber': result["blockNumber"],
        }
    elif event_name == 'Aave_v1_repay':
        
        if return_header:
            return "transactionHash,user,repayer,asset,amountMinusFees,fees,borrowBalanceIncrease,blockNumber"
        
        asset = '0x' + result["topics"][1].hex().lstrip('0x').rjust(40,'0')
        
        result_dict = {
            'transactionHash' : result["transactionHash"].hex(),
            'user': '0x' + result["topics"][2].hex().lstrip('0x').rjust(40,'0'),
            'repayer': '0x' + result["topics"][3].hex().lstrip('0x').rjust(40,'0'),
            'asset': ASSET_ADDRESSES[asset] if asset in ASSET_ADDRESSES.keys() else asset,
            'amountMinusFees': int(result["data"][:66], base=16),
            'fees': int(result["data"][67:130], base=16),
            'borrowBalanceIncrease': int(result["data"][131:194], base=16),
            'blockNumber': result["blockNumber"],
        }
    elif event_name == 'Aave_v2_repay':
        
        if return_header:
            return "transactionHash,user,repayer,asset,amount,blockNumber"
        
        asset = '0x' + result["topics"][1].hex().lstrip('0x').rjust(40,'0')
        
        result_dict = {
            'transactionHash' : result["transactionHash"].hex(),
            'user': '0x' + result["topics"][2].hex().lstrip('0x').rjust(40,'0'),
            'repayer': '0x' + result["topics"][3].hex().lstrip('0x').rjust(40,'0'),
            'asset': ASSET_ADDRESSES[asset] if asset in ASSET_ADDRESSES.keys() else asset,
            'amount': int(result["data"], base=16),
            'blockNumber': result["blockNumber"],
        }
    elif event_name == 'Aave_v3_borrows':
        # Same as Aave_v2_borrows

        if return_header:
            return "transactionHash,blockNumber"

        result_dict = {
            'transactionHash': result["transactionHash"].hex(),
            'blockNumber': result["blockNumber"],
        }
    elif event_name == 'Aave_v3_withdraws':
        # Same as Aave_v2_withdraws

        if return_header:
            return "transactionHash,blockNumber"

        result_dict = {
            'transactionHash': result["transactionHash"].hex(),
            'blockNumber': result["blockNumber"],
        }
    else:
        print(f"No event found with name {event_name}")
        return
    return result_dict