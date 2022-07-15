import pandas as pd

FILE = "results/aave3_liquidations.csv"

df = pd.read_csv(FILE)

print(df['collateralAsset'].value_counts())

print(df['debtAsset'].value_counts())

print(df['debtToCover'].median())