from web3.auto import w3
import json

# Read Asset Addresses from .json file
with open("utils/asset_addresses.json", 'r') as jsonfile:
    ASSET_ADDRESSES = json.load(jsonfile)

def get_compound_event(result, event_name="Compound_v2_liquidations", return_header=False):
    if event_name == 'Compound_v1_liquidations':
        
        if return_header:
            return "transactionHash,userLiquidated,collateralAsset,debtAsset," + \
                "liquidator,debtToCover,liquidatedCollateralAmount,blockNumber"
        

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
        
        if return_header:
            return "transactionHash,userLiquidated,collateralAsset," + \
                "liquidator,debtToCover,liquidatedCollateralAmount,blockNumber"

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
    elif event_name == 'Compound_v1_repay':
        
        if return_header:
            return "transactionHash,repayer,asset," + \
                "amount,startingBalance,newBalance,blockNumber"

        asset = '0x' + result["data"][90:130]
        
        result_dict = {
            'transactionHash' : result["transactionHash"].hex(),
            'repayer' : '0x' + result["data"][26:66],
            'asset' : ASSET_ADDRESSES[asset] if asset in ASSET_ADDRESSES.keys() else asset,
            'amount' : int(result["data"][130:194], base=16),
            'startingBalance' : int(result["data"][195:258], base=16),
            'newBalance' : int(result["data"][270:322], base=16),
            'blockNumber' : result["blockNumber"],
        }
    elif event_name == 'Compound_v2_repay':
        
        if return_header:
            return "transactionHash,repayer,borrower," + \
                "repayAmount,accountBorrows,totalBorrows,blockNumber"

        ## No asset information in this event

        result_dict = {
            'transactionHash' : result["transactionHash"].hex(),
            'repayer' : '0x' + result["data"][26:66],
            'borrower': '0x' + result["data"][90:130],
            'repayAmount' : int(result["data"][130:194], base=16),
            'accountBorrows' : int(result["data"][195:258], base=16),
            'totalBorrows' : int(result["data"][270:322], base=16),
            'blockNumber' : result["blockNumber"],
        }
    elif event_name == 'Compound_v1_deposits':

        if return_header:
            return "transactionHash,blockNumber"

        # No asset information in this event

        result_dict = {
            'transactionHash': result["transactionHash"].hex(),
            'blockNumber': result["blockNumber"],
        }

    elif event_name == 'Compound_v2_deposits':

        if return_header:
            return "transactionHash,blockNumber"

        # No asset information in this event

        result_dict = {
            'transactionHash': result["transactionHash"].hex(),
            'blockNumber': result["blockNumber"],
        }

    elif event_name == 'Compound_v1_withdraws':

        if return_header:
            return "transactionHash,blockNumber"

        # No asset information in this event

        result_dict = {
            'transactionHash': result["transactionHash"].hex(),
            'blockNumber': result["blockNumber"],
        }

    elif event_name == 'Compound_v2_withdraws':

        if return_header:
            return "transactionHash,blockNumber"

        # No asset information in this event

        result_dict = {
            'transactionHash': result["transactionHash"].hex(),
            'blockNumber': result["blockNumber"],
        }

    elif event_name == 'Compound_v1_borrows':

        if return_header:
            return "transactionHash,blockNumber"

        # No asset information in this event

        result_dict = {
            'transactionHash': result["transactionHash"].hex(),
            'blockNumber': result["blockNumber"],
        }

    elif event_name == 'Compound_v2_borrows':

        if return_header:
            return "transactionHash,blockNumber"

        # No asset information in this event

        result_dict = {
            'transactionHash': result["transactionHash"].hex(),
            'blockNumber': result["blockNumber"],
        }
    else:
        print(f"No event found with name {event_name}")
        return
    return result_dict