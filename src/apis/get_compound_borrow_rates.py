import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import time


def borrow_rates(asset_name: str, asset_address: str,
                 start_date: str, end_date: str, k: int):
    """Compound Tokens Borrow Rates into .csv

    Args:
        asset_name (str): name of the asset/token
        asset_address (str): hex address of the asset/token
        start_date (str): start date of query
        end_date (str): end date of query
        k (int): helping index for filename
    """
    
    
    url = "https://api.compound.finance/api/v2/market_history/graph"

    # UNIX time
    start_timestamp = int(pd.Timestamp(start_date).timestamp())
    end_timestamp = int(pd.Timestamp(end_date).timestamp())

    # How many buckets will the result be split into
    buckets = 1000

    headers = {
        'content-type': 'application/json',
        'accept': 'application/json',
    }

    df = pd.DataFrame({})

    for t in tqdm(range(start_timestamp, end_timestamp, 200000)):
        # Don't overuse the API
        time.sleep(2)
        
        params = {
            "asset": asset_address,
            "min_block_timestamp": t,
            "max_block_timestamp": min(end_timestamp, t + 200000),
            "num_buckets": buckets,
        }
        
        response = requests.request("GET", url, headers=headers, params=params)
        resp = response.json()
        
        # Check that a valid result is returned
        if "borrow_rates" in resp.keys() and resp["borrow_rates"]:
            d = resp["borrow_rates"]

            df1 = pd.DataFrame(d)
            df1 = df1[["block_timestamp", "rate"]]
            df = pd.concat([df,df1])   
            
            # So as not to lose the progress so far (temp fix)
            df.to_csv(f"results/rates/{asset_name}_rates_{k}.csv", index=False)
        else:
            continue

    df = df.rename(columns = {'rate': asset_name})

    df['dates'] = pd.to_datetime(df['block_timestamp'], unit='s',
                                utc=True).astype('datetime64[ns, America/New_York]')
    df.drop(columns=['block_timestamp'], axis=1, inplace=True)

    df.to_csv(f"results/rates/{asset_name}_rates_{k}.csv", index=False)


if __name__ == "__main__":
    
    # DATE FORMAT 
    START_DATE = "2021-01-01"
    END_DATE = "2021-12-31"

    assets = {
        # Make sure it's a compound asset (c prefix)
        "cETH"  : "0x4Ddc2D193948926D02f9B1fE9e1daa0718270ED5", # Done
        "cUSDC" : "0x39AA39c021dfbaE8faC545936693aC917d5E7563", # Done
        "cDAI"  : "0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643", # Done
        "cWBTC" : "0xC11b1268C1A384e55C48c2391d8d480264A3A7F4", # Done
        "cUSDT" : "0xf650C3d88D12dB855b8bf7D11Be6C55A4e07dCC9", # Done
        "cUNI"  : "0x35A18000230DA775CAc24873d00Ff85BccdeD550", # Done
    }
    
    for asset_name, asset_address in assets.items():
        borrow_rates(asset_name, asset_address, START_DATE, END_DATE, k=2)
        
        # 1 hour between query for each token to avoid ban
        time.sleep(60*60)
