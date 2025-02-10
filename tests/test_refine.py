import pprint
import requests

url = "http://127.0.0.1:8000/refine"  # Note: no trailing slash

payload = {
    "description": "apple ear pod pro 2",
    #"seller_address": "Somerset, NJ",
    "seller_persona": "old man 88 years old",
    "item_condition": "new",
    #"temperature": 0.7
}

response = requests.post(url, json=payload)
#print(f"Status Code: {response.status_code}")
pprint.pprint(response)