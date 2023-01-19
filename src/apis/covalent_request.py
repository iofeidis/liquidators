import requests
import pandas as pd
import time


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
        'no-logs': 'true',
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
        
        # Response dict to DataFrame
        df1 = pd.DataFrame(items)

        # Keep only specific columns
        df1 = df1[['from_address', 'to_address', 'value',
                'gas_spent', 'successful', 'block_height']]
        
        # Add the new data to the existing DataFrame    
        df = pd.concat([df,df1])

        # We redifine indexes
        df.index=range(0,len(df)) 

        # If False, no more data to show
        if response_dict['data']['pagination']['has_more'] == False:
            break

        # Go to next page from results
        params['page-number'] += 1
        
        # 1 Request per second (limit 5 requests/second)
        time.sleep(1)
        
    # Create .csv file
    df.to_csv(CSV_FILE, index=False)
