# Scraping Ethereum

Various python scripts for scraping the Ethereum Blockchain either by interacting with a local Ethereum node or web APIs.

## Querying Ethereum Log Events

Information about the events supported currently can be seen in the corresponding modules `src/events/<protocol_name>_events.py`.

1. First define your parameters (like `START/END_BLOCK`, `EVENT_NAME`, `FILEPATH`, etc.) by editing `src/run_query.py`

2. Either choose from the provided `EVENTS` or provide your own event signature for filtering.

3. Then save and run `python src/run_query.py`

4. Corresponding result will be saved in `FILEPATH` .csv files.

## Analyzing Events

`src/analysis.py` module provides an interactive way to analyze the event .csv files cell-by-cell (like Jupyter Notebooks).

## Working with APIs

In the `src/apis` folder there are scripts for interacting with various Ethereum APIs for extracting different information.
These scripts currently provide ways for retrieving information regarding:

* Getting all transactions for a single address
* Retrieving marketcap for specific token
* Retrieving info for specific token
* Getting history of total crypto market cap

Simply just edit these scripts with your own arguments and run them with `python src/scripts/<script_name>.py`.