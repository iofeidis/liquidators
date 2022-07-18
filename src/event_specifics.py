from web3.auto import w3
import json
from events.aave_events import get_aave_event

## This is Event Signature specific
def get_event_values(result, event_name):
    """
    Returns the values of the corresponding event

    Args:
        result (list): List containing the AttributeDict of each event
        event_name (str): Name of the specific event

    Returns:
        dict: A dict containing the values of the result
    """
    
    if event_name.split('_')[0] == 'Aave':
        result_dict = get_aave_event(result, event_name)
    else:
        print(f"No event found with name {event_name}")
        return
    return result_dict