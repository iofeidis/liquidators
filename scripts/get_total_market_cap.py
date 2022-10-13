import requests
import json

url = "https://api.livecoinwatch.com/overview/history"

payload = json.dumps({
  "currency": "USD",
  # UNIX time
  "start":1606232700000,
  "end":1606233000000,
})
headers = {
  'content-type': 'application/json',
  # API-key
  'x-api-key': 'f0f51009-9762-4f1d-a1d9-e6f5d07217f6'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
