import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

# DATE FORMAT 
START_DATE = "2022-11-01"
END_DATE = "2022-12-10"

ASSET = "0x4Ddc2D193948926D02f9B1fE9e1daa0718270ED5"
ASSET_NAME = "ETH"

url = "https://api.compound.finance/api/v2/market_history/graph"

# UNIX time
start_timestamp = int(pd.Timestamp(START_DATE).timestamp())
end_timestamp = int(pd.Timestamp(END_DATE).timestamp())

buckets = 1000

headers = {
    'content-type': 'application/json',
    'accept': 'application/json',
}

df = pd.DataFrame({})

for t in tqdm(range(start_timestamp, end_timestamp, 200000)):
    
    params = {
        "asset": ASSET,
        "min_block_timestamp": t,
        "max_block_timestamp": min(end_timestamp, t + 200000),
        "num_buckets": buckets,
    }
    
    response = requests.request("GET", url, headers=headers, params=params)
    resp = response.json()
        
    if "borrow_rates" in resp.keys() and resp["borrow_rates"]:
        d = resp["borrow_rates"]

        df1 = pd.DataFrame(d)
        df1 = df1[["block_timestamp", "rate"]]
        df = pd.concat([df,df1])   
    else:
        continue

df = df.rename(columns = {'rate': ASSET_NAME})

df['dates'] = pd.to_datetime(df['block_timestamp'], unit='s',
                            utc=True).astype('datetime64[ns, America/New_York]')
df.drop(columns=['block_timestamp'], axis=1, inplace=True)


df.to_csv(f"results/rates/{ASSET_NAME}_rates.csv", index=False)