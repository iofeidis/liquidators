from web3.auto import w3
import json
from events.aave_events import get_aave_event
from events.maker_events import get_maker_event
from events.compound_events import get_compound_event
from events.liquity_events import get_liquity_event

## This is Event Signature specific
def get_event_values(result, event_name, return_header=False):
    """
    Returns the values of the corresponding event

    Args:
        result (list): List containing the AttributeDict of each event
        event_name (str): Name of the specific event

    Returns:
        dict: A dict containing the values of the result
    """
    
    if event_name.split('_')[0] == 'Aave':
        result_dict = get_aave_event(result, event_name, return_header)
    elif event_name.split('_')[0] == 'Maker':
        result_dict = get_maker_event(result, event_name, return_header)
    elif event_name.split('_')[0] == 'Compound':
        result_dict = get_compound_event(result, event_name, return_header)
    elif event_name.split('_')[0] == 'Liquity':
        result_dict = get_liquity_event(result, event_name, return_header)
    else:
        print(f"No event found with name {event_name}")
        return
    return result_dict