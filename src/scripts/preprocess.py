import pandas as pd
import numpy as np
from web3.auto import w3
from tqdm import tqdm

# FILE = "results/test.csv"

def add_dates_to_csv(filepath: str):
    """ Add dates to .csv file based on block number

    Args:
        filepath (str): filename path
    """
    df = pd.read_csv(filepath)

    # Sort df by blockNumber
    df = df.sort_values('blockNumber')

    timestamps = []

    print("\n##### Adding dates ######")
    for i in tqdm(df.blockNumber):
        timestamps.append(w3.eth.get_block(i).timestamp)

    df['timestamps'] = timestamps

    df['dates'] = pd.to_datetime(df['timestamps'], unit='s', utc=True).astype('datetime64[ns, America/New_York]')

    df.drop(columns=['timestamps'], axis=1, inplace=True)

    df.to_csv(filepath, index=False)


def amounts_to_usd(event_assets):
    """Converts amounts of stablecoins 
    found in a DataFrame column to USD

    Args:
        event_assets: string array containing:
        * event_name
        * asset column
        * amounts column
    """
    
    #STEPS:
    # 1. Find stablecoin's name (or address)
    # 2. Find this stablecoin's number of decimals
    # 3. Do the corresponding division by number of decimals
    # 4. Create new column (named "USD")
    
    ASSETS = event_assets[1]
    AMOUNTS = event_assets[2]
    filepath = f"results/events/{event_assets[0]}.csv"
    
    temp_decimals = {
        "USDC": 6,
        "USDT": 6,
        "DAI" : 18,
        "GUSD": 2,
        "BUSD": 18,
        # "WETH": 18,
        "TUSD": 18,
        "sUSD": 18, 
    }
    
    df = pd.read_csv(filepath)
    
    df[f"{ASSETS}_decimals"] = df[ASSETS].map(lambda x: int(temp_decimals[x]) if x in temp_decimals.keys() else 0)
    
    df[f"{AMOUNTS}_USD"] = df.apply(lambda x: x[AMOUNTS][:-x[f"{ASSETS}_decimals"]] if x[f"{ASSETS}_decimals"] > 0 else -1, 1)
    
    df[f"{AMOUNTS}_USD"] = pd.to_numeric(df[f"{AMOUNTS}_USD"], downcast="integer")
    
    df.to_csv(filepath, index=False)

    
if __name__ == "__main__":
    
    # [event_name, asset, amounts]
    EVENTS = [
          ['Aave_v1_liquidations', 'debtAsset', 'debtToCover'],
          ['Aave_v3_liquidations', 'debtAsset', 'debtToCover'],
          ['Aave_v2_flashloans', 'asset', 'amount'],
          ['Aave_v1_deposits', 'asset', 'amount'],
          ['Aave_v2_deposits', 'asset', 'amount'],
          ['Aave_v1_repay', 'asset', 'amountMinusFees'],
          ['Aave_v2_repay', 'asset', 'amount'],
          ['Compound_v1_liquidations', 'debtAsset', 'debtToCover'],
        #   ['Compound_v2_liquidations'],
          ['Compound_v1_repay', 'asset', 'amount'],
        #   ['Compound_v2_repay'],
        #   ['Maker_v1_Bite'], all debt is probably in DAI
        #   ['Maker_v2_Bark'], all debt is probably in DAI
        #   ['Liquity_liquidations'],
          ]
    
    for i in EVENTS:
        print(i)
        amounts_to_usd(i)