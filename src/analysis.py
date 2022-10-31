## Script for analytics on results
## in Jupyter Cell structure

#%%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#%%
FILE = "../results/aave_liquidations.csv"

df = pd.read_csv(FILE)

print(df.head())

#%%
#### Collateral Assets #####

# Print number of unique Collateral Assets
print(f"Unique Collateral Assets: {df['collateralAsset'].nunique()}")

# Print all Collateral Assets and their value counts
print(df['collateralAsset'].value_counts())

#%%
#### Borrowed Assets #####

# Print number of unique Borrowed Assets
print(f"Unique Borrowed Assets: {df['debtAsset'].nunique()}")

# Print all Borrowed Assets and their value counts
print(df['debtAsset'].value_counts())

# %%
#### Liquidators #####

# Print number of unique Liquidator addresses
print(f"Unique Liquidators: {df['liquidator'].nunique()}")

# Percentage of liquidations triggered by top 50 Liquidators
top = 50
p = round(df['liquidator'].value_counts().head(top).sum() /
          len(df) * 100, 4)
print(f"% of liquidations triggered by top {top} Liquidators: {p}%")

# %%
#### Users Liquidated #####

# Print number of unique Collateral Assets
print(f"Unique Users Liquidated: {df['userLiquidated'].nunique()}")

# %%
#### Transaction Volume vs Announcements #####

# Number of Daily Transactions in Ethereum (from etherscan)
df_transactions = pd.read_csv("../results/total_daily_transactions.csv")
df_transactions['Date(UTC)'] = pd.to_datetime(df_transactions['Date(UTC)'])

# Dates of Announcements
df_anns = pd.read_csv("../utils/announcements.csv")

# Querying only transactions after October 2020
df_transactions = df_transactions.query('UnixTimeStamp > 1604171711')

ax = df_transactions.plot(x="Date(UTC)", y="Value")

# Adding vertical lines for the Announcements
for i in pd.to_datetime(df_anns.anns.values):
    plt.axvline(x=i, color='red', linewidth=0.4, linestyle='--')

plt.xlabel("Time")
plt.ylabel("# of Daily Transactions")

# plt.savefig('transactions.jpg', dpi=200, bbox_inches='tight')
plt.show()

# %%
###### Events vs Announcements ######
df['dates'] = pd.to_datetime(df['dates'], utc=True)
ax = df.groupby(df.dates.dt.date).size().plot(x_compat = True)

# Adding vertical lines for the Announcements
for i in pd.to_datetime(df_anns.anns.values):
    plt.axvline(x=i, color='red', linewidth=0.4, linestyle='--')

plt.xlabel("Time")
plt.ylabel("# of Events")
plt.xticks(rotation=90)

# plt.savefig('../results/Aave_Liquidations_vs_Announcements.jpg', dpi=200, bbox_inches='tight')
plt.show()
# %%
