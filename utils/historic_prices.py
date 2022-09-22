import pandas as pd
import requests
from datetime import datetime
import json

# First liquidation (in Aave) is after this date
# START_TIMESTAMP = "25.11.2019 10:00" # day.month.year hour:minutes
START_TIMESTAMP = "29.8.2022 10:00" # day.month.year hour:minutes

END_TIMESTAMP = "31.8.2022 10:00"

# Asset to be queried
# ASSET = "multi-collateral-dai"

# Preferred time interval
# Options : m1, m5, m15, m30, h1, h2, h6, h12, d1
# where m=minute, h=hour, d=day
INTERVAL = "d1"

# Need to convert date timestamps to unix milliseconds
dt_obj_start = datetime.strptime(START_TIMESTAMP,'%d.%m.%Y %H:%M')
dt_obj_end = datetime.strptime(END_TIMESTAMP,'%d.%m.%Y %H:%M')

start_timestamp = str(int(dt_obj_start.timestamp() * 1000))
end_timestamp = str(int(dt_obj_end.timestamp() * 1000))


coincap_df = pd.read_csv("utils/coincap_top100_ids.csv")

payload={}
headers = {}

df_total = pd.DataFrame({'timestamp': []})

for i, id in enumerate(coincap_df['id'][::-1]):
    url = f"http://api.coincap.io/v2/assets/{id}/history?interval={INTERVAL}&start={start_timestamp}&end={end_timestamp}"
    
    response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.text)
    data = json.loads(response.text)
    # print(data)
    
    timestamps = [k['time'] for k in data['data']]
    prices = [round(float(k['priceUsd']),3) for k in data['data']]
    
    symbol = coincap_df.loc[coincap_df['id'] == id,].reset_index().at[0, 'symbol']
    
    df1 = pd.DataFrame(zip(timestamps, prices), columns=['timestamp', symbol])
    
    df_total = df1.merge(df_total, how='outer', on='timestamp', sort='timestamp')
    
print(df_total)

# df_total.to_csv("utils/historical_prices.csv", index=False)