from multiprocessing.context import assert_spawning
import requests
import json
import pandas as pd
import csv

EVENTS_FILE = "results/compound_v2_liquidations.csv"
OUTPUT_FILE = "results/tokens_2.csv"

df = pd.read_csv(EVENTS_FILE)

with open(OUTPUT_FILE, 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow("token,symbol".split(','))
    
    for token in  df.collateralAsset.value_counts().keys().tolist():
        if token[:2] != "0x":
            continue
        url = f"https://api.ethplorer.io/getTokenInfo/{token}?apiKey=freekey"

        response = requests.get(url)
        if response.status_code == 200 and 'application/json' in response.headers.get('Content-Type',''):
            spamwriter.writerow([token, response.json()["symbol"]])