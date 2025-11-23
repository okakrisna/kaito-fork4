import requests

# Test admin panel kaito2 content loading
response = requests.get('http://localhost:5001/api/pages/kaito2/content')
data = response.json()

print(f"Status: {response.status_code}")
print(f"Success: {data.get('success')}")
print(f"Page name: {data.get('page_info', {}).get('name')}")
print(f"Content fields: {len(data.get('content', {}))}")
print(f"External link: {data.get('page_info', {}).get('external_link')}")