import pandas as pd
from web3.auto import w3

# FILE = "results/test.csv"

def add_dates_to_csv(filepath: str="results/test.csv"):
    """ Add dates to .csv file based on block number

    Args:
        filepath (str): filename path
    """
    df = pd.read_csv(filepath)

    # Sort df by blockNumber
    df = df.sort_values('blockNumber')

    timestamps = []

    for i in df.blockNumber:
        timestamps.append(w3.eth.get_block(i).timestamp)
        if i % 1000 == 0:
            print(f"Adding date to block: {i}")

    df['timestamps'] = timestamps

    df['dates'] = pd.to_datetime(df['timestamps'], unit='s', utc=True).astype('datetime64[ns, America/New_York]')

    df.drop(columns=['timestamps'], axis=1, inplace=True)

    df.to_csv(filepath, index=False)
