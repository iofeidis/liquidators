from web3.auto import w3
from queries.logs_query import run_query
from scripts.add_dates_to_csv import add_dates_to_csv


START_BLOCK = 7000000
# Check what JSON-RPC thinks as the latest block number
END_BLOCK = 15960000

EVENTS = [
        #   'Aave_v1_liquidations'
        #   'Aave_v3_liquidations',
        #   'Aave_v2_flashloans',
        #   'Compound_v2_liquidations',
        #   'Compound_v1_liquidations',
        #   'Maker_v1_Bite',
        #   'Maker_v2_Bark',
          'Liquity_liquidations'
          ]

# EVENT_NAME = 'Kick(uint256,uint256,uint256,uint256,address,address,uint256)'
# EVENT_NAME = 'Take(uint256,uint256,uint256,uint256,uint256,uint256,address)'
# EVENT_NAME = 'Kick(uint256,uint256,uint256,uint256,address,address,uint256)'
# EVENT_NAME = 'Take(uint256,uint256,uint256,uint256,uint256,uint256,address)'
# EVENT_NAME = 'Kick(uint256,uint256,uint256,uint256,address,address)'
# EVENT_NAME = 'LogNote(bytes4,address,bytes32,bytes32,bytes)'
# EVENT_NAME = 'LogTrade(uint,address,uint,address)'
# EVENT_NAME = 'Bite(bytes32,address,uint256,uint256,uint256,address,uint256)'
# EVENT_NAME = 'LiquidateBorrow(address,address,uint256,address,uint256)'
# EVENT_NAME = 'BorrowLiquidated(address,address,uint256,uint256,uint256,uint256,address,address,uint256,uint256,uint256,uint256)'
# EVENT_NAME = 'SupplyReceived(address,address,uint256,uint256,uint256)'
# EVENT_NAME = 'TroveLiquidated(address,uint256,uint256,uint8)'


if __name__=="__main__":
    
    # Check if node is connected
    print(f"Node is connected : {w3.isConnected()}")
    
    for event_name in EVENTS:
        
        print(f"Current event: {event_name}")
        
        FILEPATH = f"results/events/{event_name}.csv"
        
        ## DEBUG
        # FILEPATH = f"results/events/test.csv"
    
        # Run the query and save the result to filepath
        run_query(filepath=FILEPATH, start_block=START_BLOCK,
                end_block=END_BLOCK, event_name=event_name)

        print("Done run_query")
        
        # Add dates to query result
        add_dates_to_csv(filepath=FILEPATH)
        
    