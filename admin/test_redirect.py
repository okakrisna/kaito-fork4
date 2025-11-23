import requests

response = requests.get('http://localhost:5001/api/pages/kaito2/content')
data = response.json()

print(f"Success: {data.get('success')}")
print(f"External link: {data.get('page_info', {}).get('external_link')}")
print(f"Page name: {data.get('page_info', {}).get('name')}")