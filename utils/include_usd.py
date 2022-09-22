import pandas as pd

EVENTS_FILE = "results/aave_liquidations.csv"
TOTAL_PRICES_FILE = "utils/total_prices.csv"
IDS_FILE = "utils/coincap_top100_ids.csv"


df_events = pd.read_csv(EVENTS_FILE)

df_prices = pd.read_csv(TOTAL_PRICES_FILE)

df_ids = pd.read_csv(IDS_FILE)


debtasset_at_block = [(i, j) for i,j in zip(df_events.debtAsset, df_events.block)]
df_events.debtAssetParity = pd.Series([df_prices.at[i, j] for i, j in debtasset_at_block])

ids_not_present = [i for i in df_events.debtAsset.unique() if i not in df_ids.symbol.values]

debtAssetParity = []
for i,j in debtasset_at_block:
    if i in ids_not_present:
        debtAssetParity.append(-1)
    else:
        debtAssetParity.append(df_prices.at[i,j])

df_events['debtAssetParity'] = pd.Series(debtAssetParity)