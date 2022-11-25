import requests
import pandas as pd
import time
import csv

def call_covalent(protocol_address, COVALENT_API_KEY):   
    ## Request Arguments
    url_string = f'https://api.covalenthq.com/v1/1/address/{protocol_address}/transactions_v2/'

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
    
    # manually deciding that after 10 consecutive errors the loops will be terminated
    error_number = 0 
    
    ## Iterate over result pages
    while True:
        response = requests.get(url_string,
            params=params, headers=headers, auth=auth)
        print(f"Number {params['page-number']} Page of Results")
        
        # API response to dictionary
        print("response: ", response)
        
        try:
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

            # After drop there are missing rows and indexes. We redifine indexes
            df.index=range(0,len(df)) 

            # print("After concating: ", df.iloc[0,:])
            print("After concating: ", df.head())
            print("After concating: ", df.tail())

            # If False, no more data to show
            if response_dict['data']['pagination']['has_more'] == False:
                break

            # Go to next page from results
            params['page-number'] += 1
            error_number =0 
            
            # 1 Request per second (limit 5 requests/second)
        except Exception as e: 
            print(e)
            params['page-number'] += 1
            error_number += 1
            print("error_number: ",error_number)
            if(error_number>10):
                break
        time.sleep(10)

    # return dataframe to be writen in a csv file
    return df

if __name__ == "__main__":
  
    COVALENT_API_KEY = "ckey_a1e61633400a49bdaffd08459af"
    CSV_FILE_PATH = "results/transactions/"
    CSV_SMALL_FILES_PATH = "results/transactions_small/"
    addresses_file = "input/address_files/aaveV2-small.txt"
    contract_address = "0x39c6b3e42d6a679d7d776778fe880bc9487c2eda"

    with open(addresses_file) as fp:
        reader = csv.reader(fp, delimiter=";", quotechar='"')
        data_read = [row for row in reader]
        for row in data_read:
            contract_address = row[0]
            contract_name = row[1]
            csv_file = CSV_FILE_PATH + contract_address + "---" + contract_name + ".csv"
            print("Retrieving data for: ",csv_file)
            df = call_covalent(contract_address, COVALENT_API_KEY)
            
            # Create the big .csv file
            print("final df for all transactions csv:", df.head(), df.tail())
            print("Writing file :", csv_file)
            df.to_csv(csv_file, index=False)


            #create smaller csv containing only transactions where address is in from_address or to_address
            csv_file_small = CSV_SMALL_FILES_PATH + contract_address + "---" + contract_name + ".csv"
            print("Writing file :", csv_file_small)

            print("Dataframe before length: ", len(df.index))
            print("df before: ",df[["from_address","to_address"]])

            df = df.drop(df[(df.from_address != contract_address) & (df.to_address != contract_address)].index)
            
            # After drop there are missing rows and indexes. We redifine indexes
            df.index=range(0,len(df)) 
            print("df after: ",df[["from_address","to_address"]])
            print("Dataframe after length: ", len(df.index))

            df.to_csv(csv_file_small, index=False)




