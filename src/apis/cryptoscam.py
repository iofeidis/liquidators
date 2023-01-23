import json
import pandas as pd
from web3.auto import w3
import requests

def api_request(filename: str):
    """Cryptoscam malicious addresses API result to json

    Args:
        filename (str): name of .json file
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
    """Preprocess .json file with results 
    from cryptoscam.db

    Args:
        filename (str): name of .json file
    """
    with open(f"utils/{filename}", "r") as outfile:
        json_object = json.load(outfile)
    
    # Hex Malicious Addresses
    adds = []
    for k,v in json_object['result'].items():
        if v[0]["category"] in ["Phishing", "Scamming"]:
            if k[:2] == "0x" and len(k) == 42:
                adds.append(k)
    
    print(f"Node Connected: {w3.isConnected()}")
    tx_counts = [w3.eth.get_transaction_count(w3.toChecksumAddress(i)) 
                    for i in adds]

    df = pd.DataFrame({"address": adds, "tx_count": tx_counts})

    df.to_csv("results/cryptoscam_adds.csv", index=False)
    

def add_labels(nodes_file: str, adds_file: str):
    """Add labels to nodes.csv file

    Args:
        nodes_file (str): name of nodes file
        adds_file (str): file containing all malicious addresses
                        from cryptoscam.db
    """
    
    # Read malicious addresses .csv file 
    with open(f"{adds_file}", "r") as outfile:
        adds = pd.read_csv(outfile)

    # Set index for quicker lookup
    adds = adds.set_index("address")

    # Read nodes.csv
    with open(f"{nodes_file}", "r") as outfile:
        nodes = pd.read_csv(outfile)

    # Set index for quicker lookup
    nodes = nodes.set_index("address")

    # Lookup
    # Add labels to nodes by mapping on adds
    nodes['Label_crscam'] = nodes.index.map(lambda x: "Bad" if str(x).lower() in adds.index else "Good")
    
    # Reset index to column "address"
    nodes.reset_index(level=0, inplace=True)
    
    # Hardcoded filename for labeled nodes
    nodes.to_csv(f"results/nodes_labeled.csv", index=False)
    


if __name__ == "__main__":
    
    filename = "crypto_scam.json"
    
    # api_request(filename) # File already downloaded
    
    # preprocess_json(filename)
    
    add_labels(nodes_file="results/nodes_2.csv", 
               adds_file="results/malicious_adds.csv")