import csv, os
from google.cloud import bigquery
from event_signatures import EVENT_SIGNATURES
from web3.auto import w3

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../bigquery_key.json"
client = bigquery.Client()

EVENT_SIGNATURE = EVENT_SIGNATURES['Aave_v3_liquidations']
event_signature = w3.keccak(text=EVENT_SIGNATURE).hex()

QUERY = \
f"""
CREATE TEMP FUNCTION from_hex_to_intstring(hex STRING)
RETURNS STRING   
LANGUAGE js AS r'yourNumber = BigInt(hex,16); return yourNumber;';

SELECT 
  transaction_hash,
  '0x' || SUBSTRING(data, 155, 40) AS liquidator,
  from_hex_to_intstring(SUBSTRING(data, 1, 66)) AS debtToCover,
  from_hex_to_intstring('0x' || SUBSTRING(data, 67, 64)) AS liquidatedCollateralAmount,
  block_number,
  blocks.timestamp
FROM `bigquery-public-data.crypto_ethereum.logs` AS logs
JOIN `bigquery-public-data.crypto_ethereum.blocks` AS blocks
  ON logs.block_number=blocks.number
WHERE DATE(block_timestamp) < '2022-07-07' AND
      DATE(block_timestamp) > '2015-10-01' AND
      topics[SAFE_OFFSET(0)] = '{event_signature}';
"""

FILE = "results/aave3_liquidations.csv"
HEADER = "transaction_hash,liquidator,debtToCover,liquidatedCollateralAmount,block_number"
DESTINATION_TABLE="delta-basis-350021.dataset_01.table_05"

with open(FILE, 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(HEADER.split(","))

    job_config = bigquery.QueryJobConfig(allow_large_results=True,destination=DESTINATION_TABLE)
    query_job = client.query(
        QUERY,
        # Location must match that of the dataset(s) referenced in the query.
        location='US',
        job_config=job_config)  # API request - starts the query
    query_job.result() # Wait for the job to complete

    for item in query_job:
        spamwriter.writerow(item)
