import pandas as pd
import os
from web3.auto import w3
from tqdm import tqdm
import csv
import requests, time

# from apis/many_files_covalent_request.py
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
        'no-logs': 'false',
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
            
            # Iterate through all the transactions returned from the response
            for item_index in range(len(items)):
                
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
            df1 = df1[['block_signed_at','from_address', 'to_address', 'value', 'events',
                    'gas_spent', 'successful', 'block_height' #,'tx_hash'
                    ]]

            # Add the new data to the existing DataFrame    
            df = pd.concat([df,df1])

            # After drop there are missing rows and indexes. We redifine indexes
            df.index=range(0,len(df)) 

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
        time.sleep(8)

    # return dataframe to be writen in a csv file
    return df

# from apis/many_files_covalent_request.py
def downloadTransactions(CSV_FILE_PATH, CSV_SMALL_FILES_PATH, addresses_file):
    COVALENT_API_KEY = "ckey_a1e61633400a49bdaffd08459af"
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
            print("df for all transactions csv:", df.tail())
            print("Writing file :", csv_file)
            df.to_csv(csv_file, index=False)

            #create smaller csv containing only transactions where address is in from_address or to_address
            csv_file_small = CSV_SMALL_FILES_PATH + contract_address + "---" + contract_name + ".csv"
            print("Writing file :", csv_file_small)

            try:
                df = df.drop(df[(df.from_address != contract_address) & (df.to_address != contract_address)].index)
                
                # After drop there are missing rows and indexes. We redifine indexes
                df.index=range(0,len(df)) 
                print("df : ",df[["from_address","to_address"]])
                print("Dataframe after length: ", len(df.index))
            except Exception as e:
                print("Error", e)

            df.to_csv(csv_file_small, index=False)
    
def add_dates_to_csv(filepath: str):
    """ Add dates to .csv file based on block number

    Args:
        filepath (str): filename path
    """
    df = pd.read_csv(filepath)
    # Sort df by blockNumber
    df = df.sort_values('block_height')

    timestamps = []

    print("\n##### Adding dates to file: ", filepath," ######")
    for i in tqdm(df.block_height):
        timestamps.append(w3.eth.get_block(i).timestamp)

    df['timestamps'] = timestamps
    df['dates'] = pd.to_datetime(df['timestamps'], unit='s', utc=True).astype('datetime64[ns, America/New_York]')
    df.drop(columns=['timestamps'], axis=1, inplace=True)
    df.to_csv(filepath, index=False)

def addProtocolNamesFromAddresses(addresses_file, transactionsFile, final_dataset_file):
   # read transactions csv to dataframe df1
   df1 = pd.read_csv(transactionsFile)  
   print(df1.tail())
   print("VALUE COUNTS:", df1['from_address'].value_counts())

   # read addresses/names csv to dataframe df2
   df2 = pd.read_csv(addresses_file) 
   print(df2.tail())

   #replace address of df1 with names from df2
   with open(addresses_file) as fp:
      reader = csv.reader(fp, delimiter=";", quotechar='"')
      data_read = [row for row in reader]
      for row in data_read:
         contract_address = row[0]
         contract_name = row[1]
         print(contract_name, contract_address)
         # print((df1.from_address == contract_address).sum())
         
         df1['from_address'].replace(contract_address, contract_name, inplace=True)
         df1['to_address'].replace(contract_address, contract_name, inplace=True)
   df1.to_csv(final_dataset_file, index=False)  

# Remove tx_hash from file
def removeColumn(addresses_file):
   df1 = pd.read_csv(addresses_file)  
   df1.drop('tx_hash', axis=1, inplace=True)
   df1.to_csv(addresses_file, index=False) 

def merge_files(directory_path, output_file, protocol_name):
   
   files = os.listdir(directory_path)

   print("In the directory",os.listdir(directory_path)," there are files: ", len(files))
   df_all = pd.DataFrame()
   for file in files:
      if os.path.isfile(os.path.join(directory_path, file)):
         print("Opening file: ", os.path.join(directory_path, file))

         try:
            df = pd.read_csv(os.path.join(directory_path, file), sep=',')
            print("Dataframe length: ", len(df.index))
            if file.endswith('.csv'):
               file = file[:-4]
            df['contract'] = file
            df['protocol_name'] = protocol_name
            print(df.head())
            df_all = pd.concat([df_all, df])
         except Exception as e:
            print(e)

   print("Writing ",len(df_all.index), "transactions to file: ", output_file)
   df_all.to_csv(output_file, index=False) 

if __name__ == "__main__":
   
   protocol_name = 'DYDX'
   transactions_folder_path = os.getcwd()+ f'/results/transactions/{protocol_name}/'
   transactions_small_folder_path = os.getcwd()+f'/results/transactions_small/{protocol_name}/'
   addresses_file = os.getcwd()+ f'/input/address_files/{protocol_name}.txt'
   final_dataset_file =  os.getcwd()+f'/results/finalDatasets/{protocol_name}.csv'
   final_dataset_small_file =  os.getcwd()+f'/results/finalDatasets-small/{protocol_name}-small.csv'

   # create folders if they don't already exist
   if not os.path.exists(transactions_folder_path):
      os.makedirs(transactions_folder_path)
   if not os.path.exists(transactions_small_folder_path):
      os.makedirs(transactions_small_folder_path)

   downloadTransactions(transactions_folder_path, transactions_small_folder_path, addresses_file)

   merge_files(transactions_folder_path, final_dataset_file, protocol_name)
   merge_files(transactions_small_folder_path, final_dataset_small_file, protocol_name)

   add_dates_to_csv(final_dataset_file)
   add_dates_to_csv(final_dataset_small_file)

   addProtocolNamesFromAddresses(addresses_file, final_dataset_file, final_dataset_file)
   addProtocolNamesFromAddresses(addresses_file, final_dataset_small_file, final_dataset_small_file)
