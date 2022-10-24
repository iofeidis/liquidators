import pandas as pd
from web3.auto import w3

FILE = "results/aave_v2_flashloans.csv"

df = pd.read_csv(FILE)

# Sort df by blockNumber
df = df.sort_values('blockNumber')

timestamps = []

for i in df.blockNumber:
    timestamps.append(w3.eth.get_block(i).timestamp)
    if i % 1000 == 0:
        print(f"Current block: {i}")

df['timestamps'] = timestamps

df['dates'] = pd.to_datetime(df['timestamps'], unit='s', utc=True).astype('datetime64[ns, America/New_York]')

df.drop(columns=['timestamps'], axis=1, inplace=True)

df.to_csv("results/aave_v2_flashloans_new.csv", index=False)
