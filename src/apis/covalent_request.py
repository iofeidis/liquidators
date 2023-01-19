import requests
import pandas as pd
import time
from tqdm import tqdm


if __name__ == "__main__":
    COVALENT_API_KEY = "ckey_a1e61633400a49bdaffd08459af"
    ADDRESS = "0x39c6b3e42d6a679d7d776778fe880bc9487c2eda"
    CSV_FILE = f"results/transactions/{ADDRESS}.csv"


    ## Request Arguments
    # https://www.covalenthq.com/docs/api/#/0/Get%20transactions%20for%20address/USD/1
    url_string = f'https://api.covalenthq.com/v1/1/address/{ADDRESS}/transactions_v2/'

    headers = {
        'Content-Type': 'application/json',
    }

    params = {
        'quote-currency': 'USD',
        # 'format': 'CSV',
        'block-signed-at-asc': 'false',
        'no-logs': 'false',
        'page-size': '1000', # Default size: 100
        'page-number': 0, # 0-based
    }

    # Covalent API Key
    auth=(COVALENT_API_KEY, '')

    # Initialize DataFrame
    df = pd.DataFrame({})
    

    ## Iterate over result pages
    while True:
            
        response = requests.get(url_string,
            params=params, headers=headers, auth=auth)
        print(f"Number {params['page-number']} Page of Results")
            
        # API response to dictionary
        response_dict = response.json()

        # Keep only data from the response
        items = response_dict['data']['items']
        

        # Iterate through all the transactions returned from the response
        for item_index in tqdm(range(len(items))):
            
            # Create Empty list
            events_of_tx = []
            
            # Iterate through all the log_events in this transaction
            for i in range(len(items[item_index]['log_events'])):
                
                # If this log_event has a name, add this name to the events_of_tx list
                if items[item_index]['log_events'][i]['decoded'] != None:
                    events_of_tx.append(items[item_index]['log_events'][i]['decoded']['name'])
            
            # Add the created list to the initial items dictionary
            items[item_index]['events'] = events_of_tx


        # Response dict to DataFrame
        df1 = pd.DataFrame(items)

        # Keep only specific columns
        df1 = df1[['from_address', 'to_address', 'value', 'events',
                'gas_spent', 'successful', 'block_height']]
        
        # Add the new data to the existing DataFrame    
        df = pd.concat([df,df1])

        # If False, no more data to show
        if response_dict['data']['pagination']['has_more'] == False:
            break

        # Go to next page from results
        params['page-number'] += 1
        
        # 1 Request per second (limit 5 requests/second)
        time.sleep(1)
        
    # Create .csv file
    df.to_csv(CSV_FILE, index=False)
