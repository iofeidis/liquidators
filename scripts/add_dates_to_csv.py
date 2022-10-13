import pandas as pd
from web3.auto import w3

FILE = "results/aave_liquidations.csv"

df = pd.read_csv(FILE)

# df = df.iloc[0:20]

timestamps = []

if df.at[len(df)-1, 'blockNumber'] > w3.eth.get_block('latest').number:
    print("Node not synced for latest blockNumber")
    print(f"Latest blockNumber in df: {df.at[len(df)-1, 'blockNumber']}")
    exit()

# Sort df by blockNumber
df = df.sort_values('blockNumber')

for i in df.blockNumber:
    timestamps.append(w3.eth.get_block(i).timestamp)
    if i % 1000 == 0:
        print(f"Current block: {i}")


df['timestamps'] = pd.Series(timestamps)

df['dates'] = pd.to_datetime(df['timestamps'], unit='s', utc=True).astype('datetime64[ns, America/New_York]')

df.drop(columns=['timestamps'], axis=1, inplace=True)

print(df)

df.to_csv("results/aave_liquidations_with_dates.csv", index=False)
