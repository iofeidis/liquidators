import json
import pandas as pd
from web3.auto import w3
import requests

def api_request(filename: str):
    """Cryptoscam malicious addresses API result to json
    """
    
    
    url = "https://api.cryptoscamdb.org/v1/addresses"

    headers = {
        'content-type': 'application/json',
        'accept': 'application/json',
    }

    response = requests.request("GET", url, headers=headers)
    print(response.text)
    resp = response.json()
    
    json_object = json.dumps(resp, indent=4)
    
    # Writing to sample.json
    with open(f"utils/{filename}", "w") as outfile:
        outfile.write(json_object)

def preprocess_json(filename: str):
    with open(f"utils/{filename}", "r") as outfile:
        json_object = json.load(outfile)
    
    # Hex Malicious Addresses
    adds = [i for i in json_object['result'].keys() 
                if i[:2] == "0x" and len(i) == 42]
    
    print(f"Node Connected: {w3.isConnected()}")
    tx_counts = [w3.eth.get_transaction_count(w3.toChecksumAddress(i)) 
                    for i in adds]
    
    


if __name__ == "__main__":
    
    filename = "crypto_scam.json"
    # api_request(filename)
    preprocess_json(filename)