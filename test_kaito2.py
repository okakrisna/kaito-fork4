import requests

# Test the editable kaito2 page
print("Testing kaito2 editable page...")
response = requests.get('http://localhost:5002/editable')
print(f"Status: {response.status_code}")
print(f"Content length: {len(response.text)}")
print(f"Has editable attributes: {'data-editable=' in response.text}")
print(f"Has Jimmy & Sherly: {'Jimmy & Sherly' in response.text}")

# Test the API
print("\nTesting kaito2 API...")
api_response = requests.get('http://localhost:5002/api/content')
api_data = api_response.json()
print(f"API Status: {api_response.status_code}")
print(f"API Success: {api_data.get('success')}")
print(f"Content keys: {list(api_data.get('content', {}).keys())[:5]}...")  # First 5 keys