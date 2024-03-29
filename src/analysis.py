## Script for analytics on results
## in Jupyter Cell structure

#%%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#%%
EVENT_NAME = "Aave_v2_repay"
FILE = f"../results/events/{EVENT_NAME}.csv"

df = pd.read_csv(FILE)
print(df.head())

#%%
#### Collateral Assets #####
asset_name = "asset"

# Print number of unique Collateral Assets
print(f"Unique Collateral Assets: {df[asset_name].nunique()}")

# Print all Collateral Assets and their value counts
print(df[asset_name].value_counts())

#%%
#### Borrowed Assets #####

# Print number of unique Borrowed Assets
print(f"Unique Borrowed Assets: {df['debtAsset'].nunique()}")

# Print all Borrowed Assets and their value counts
print(df['debtAsset'].value_counts())

# %%
#### Liquidators #####

user_name = "repayer"

# Print number of unique Liquidator addresses
print(f"Unique Liquidators: {df[user_name].nunique()}")

# Percentage of liquidations triggered by top 50 Liquidators
top = 50
p = round(df[user_name].value_counts().head(top).sum() /
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
df_transactions = df_transactions.query('UnixTimeStamp > 1539909857')

ax = df_transactions.plot(x="Date(UTC)", y="Value")

# Adding vertical lines for the Announcements
for i in pd.to_datetime(df_anns.anns.values):
    plt.axvline(x=i, color='red', linewidth=0.4, linestyle='--')

plt.xlabel("Time")
plt.ylabel("# of Daily Transactions")

plt.savefig('../results/figures/transactions.jpg', dpi=200, bbox_inches='tight')
# plt.show()

# %%
###### Events vs Announcements ######
df['dates'] = pd.to_datetime(df['dates'], utc=True)
# Querying only transactions after October 2020
df = df.loc[df.dates > df.dates[18000]]

ax = df.groupby(df.dates.dt.date).size().plot(x_compat = True)

# Dates of Announcements
df_anns = pd.read_csv("../utils/announcements.csv")

# Adding vertical lines for the Announcements
for i in pd.to_datetime(df_anns.anns.values):
    plt.axvline(x=i, color='red', linewidth=0.4, linestyle='--')

plt.xlabel("Time")
plt.ylabel("# of Events")
plt.xticks(rotation=90)

plt.savefig(f'../results/figures/{EVENT_NAME}_vs_Announcements.jpg', dpi=200, bbox_inches='tight')
# plt.show()



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
######### TVL DeFi vs Announcements ########

# Downloaded from https://defillama.com/
df_tvl = pd.read_json("../utils/data/tvl.json")
df_tvl = df_tvl.query("date > '2020-01-01'")
df_tvl.plot.line(x='date', y='totalLiquidityUSD')

# Dates of Announcements
df_anns = pd.read_csv("../utils/announcements.csv")

# # Adding vertical lines for the Announcements
for i in pd.to_datetime(df_anns.anns.values):
    plt.axvline(x=i, color='red', linewidth=0.4, linestyle='--')

plt.xlabel("Time")
plt.ylabel("Total Value Lock (USD)")
# plt.xticks(rotation=90)
plt.legend(['TVL','Announcements'])
    
plt.savefig(f'../results/figures/TVL.jpg', dpi=200, bbox_inches='tight')
# plt.show()

# %%
########## DeFi APYs vs Announcements

# Dates of Announcements
df_anns = pd.read_csv("../utils/announcements.csv")

# Daily Number of Events
df = pd.read_csv("../utils/medianAPY.csv")
df.timestamp = pd.to_datetime(df.timestamp)
df.plot(x="timestamp", y="medianAPY")

df_anns.anns = pd.to_datetime(df_anns.anns)

# Time limit
df_anns = df_anns.query("anns > '2022-01-01'")

# # Adding vertical lines for the Announcements
for i in df_anns.anns.values:
    plt.axvline(x=i, color='red', linewidth=0.4, linestyle='--')

plt.xlabel("Time")
plt.ylabel("Median APY")
# plt.xticks(rotation=90)
plt.legend(['DeFi APY','Announcements'])

plt.savefig(f'../results/figures/apys.jpg', dpi=200, bbox_inches='tight')
# plt.show()
# %%


#%%
df = pd.read_csv("../results/events_daily_counts/Aave_deposits_total.csv")
# df = df[df.is_Fed_Announcement == True]
df.dates = pd.to_datetime(df.dates)
# df = df.set_index("dates")
df = df[df.dates > "2022-05-01"]



sns.set_theme()
g = sns.lineplot(data=df, x="dates",
             y="count").get_figure().autofmt_xdate()

# g = plt.fill_between(df.index, df.count, alpha=0.2)

# sns.lineplot(data=df, x="count", hue="is_Fed_Announcement",
#              stat="density", bins=10)
plt.show()
# %%
