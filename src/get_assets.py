import requests
from datetime import datetime

START_TIMESTAMP = "4.7.2022 10:00" # day.month.year hour:minutes
END_TIMESTAMP = "10.7.2022 10:00"

# Asset to be queried
ASSET = "ethereum"

# Preferred time interval
# Options : m1, m5, m15, m30, h1, h2, h6, h12, d1
# where m=minute, h=hour, d=day
INTERVAL = "m15"

# Need to convert date timestamps to unix milliseconds
dt_obj_start = datetime.strptime(START_TIMESTAMP,'%d.%m.%Y %H:%M')
dt_obj_end = datetime.strptime(END_TIMESTAMP,'%d.%m.%Y %H:%M')

start_timestamp = str(int(dt_obj_start.timestamp() * 1000))
end_timestamp = str(int(dt_obj_end.timestamp() * 1000))

url = f"http://api.coincap.io/v2/assets/{ASSET}/history?interval={INTERVAL}&start={start_timestamp}&end={end_timestamp}"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

# Result to be printed in console
# Try `python get_assets.py | jq` for better printing
print(response.text)
