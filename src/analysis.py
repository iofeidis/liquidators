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
####### Stocks Indices vs Daily Transactions ############

### Variables ###
FILE   = "../../stock_indices.csv"
COLUMN = "nasdaq   %Change"
YLABEL = "%Change"
LEGEND = "NASDAQ Index"
#################

df_stocks = pd.read_csv(FILE)
df_stocks['Date'] = pd.to_datetime(df_stocks['Date'])
df_stocks = df_stocks.query("Date > '2020-04-01'")

fig, axs = plt.subplots(2, 1)

axs[0].plot(df_stocks['Date'], df_stocks[COLUMN])
axs[0].set_ylabel(YLABEL)
axs[0].legend([LEGEND])

# Dates of Announcements
df_anns = pd.read_csv("../utils/announcements.csv")

# # Adding vertical lines for the Announcements
for i in pd.to_datetime(df_anns.anns.values):
    axs[0].axvline(x=i, color='red', linewidth=0.4, linestyle='--')

# Number of Daily Transactions in Ethereum (from etherscan)
df_transactions = pd.read_csv("../results/total_daily_transactions.csv")
df_transactions['Date(UTC)'] = pd.to_datetime(df_transactions['Date(UTC)'])

# Querying only transactions after October 2020
df_transactions = df_transactions.query('UnixTimeStamp > 1585765455')
axs[1].plot(df_transactions["Date(UTC)"], df_transactions["Value"], color = 'black')  

# # Adding vertical lines for the Announcements
for i in pd.to_datetime(df_anns.anns.values):
    plt.axvline(x=i, color='red', linewidth=0.4, linestyle='--')

plt.xlabel("Time")
plt.ylabel("# of Daily Transactions")
# plt.xticks(rotation=90)
plt.legend(['Transactions','Announcements'])

plt.savefig(f'../results/figures/{COLUMN}.jpg', dpi=200, bbox_inches='tight')
# plt.show()



# %%
####### Stocks Indices vs Daily Events ############

### Variables ###
FILE   = "../../stock_indices.csv"
COLUMN = "s&p500  %Change"
YLABEL = "%Change"
LEGEND = "S&P500 Index"
OUTPUT = f"{COLUMN}_Compound_Liquidations"

FILE_EVENT = "../results/compound_v2_liquidations.csv"

#################

df_stocks = pd.read_csv(FILE)
df_stocks['Date'] = pd.to_datetime(df_stocks['Date'])
df_stocks = df_stocks.query("Date > '2020-04-01'")

fig, axs = plt.subplots(2, 1)

axs[0].plot(df_stocks['Date'], df_stocks[COLUMN])
axs[0].set_ylabel(YLABEL)
axs[0].legend([LEGEND])

# Dates of Announcements
df_anns = pd.read_csv("../utils/announcements.csv")

# # Adding vertical lines for the Announcements
for i in pd.to_datetime(df_anns.anns.values):
    axs[0].axvline(x=i, color='red', linewidth=0.4, linestyle='--')


# Daily Number of Events
df = pd.read_csv(FILE_EVENT)
df['dates'] = pd.to_datetime(df['dates'], utc=True)
axs[1] = df.groupby(df.dates.dt.date).size().plot(x_compat = True)

# # Adding vertical lines for the Announcements
for i in pd.to_datetime(df_anns.anns.values):
    plt.axvline(x=i, color='red', linewidth=0.4, linestyle='--')

plt.xlabel("Time")
plt.ylabel("# of Daily Events")
# plt.xticks(rotation=90)
plt.legend(['Transactions','Announcements'])

plt.savefig(f'../results/figures/{OUTPUT}.jpg', dpi=200, bbox_inches='tight')
# plt.show()


# %%
