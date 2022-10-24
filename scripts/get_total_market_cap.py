import requests
import json
import pandas as pd

# DATE FORMAT 
START_DATE = "2021-01-02"
END_DATE = "2021-01-04"

url = "https://api.livecoinwatch.com/overview/history"

payload = json.dumps({
    "currency": "USD",
    # UNIX time
    "start":int(pd.Timestamp(START_DATE).timestamp()* 1000),
    "end":int(pd.Timestamp(END_DATE).timestamp() * 1000),
})
headers = {
    'content-type': 'application/json',
    # API-key
    'x-api-key': 'f0f51009-9762-4f1d-a1d9-e6f5d07217f6'
}

response = requests.request("POST", url, headers=headers, data=payload)

df = pd.read_json(response.text)

df['date'] = df['date'].astype('datetime64[ns, America/New_York]')

print(df)

# Save the df
# df.to_csv(FILENAME, index=False)
