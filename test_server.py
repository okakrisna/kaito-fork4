#!/usr/bin/env python3

import sys
import os
sys.path.append('admin')

# Test the Flask app
from server_multi import app

# Test routes
print("Testing Flask routes...")
with app.test_client() as client:
    # Test main route
    response = client.get('/')
    print(f"Main route status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Main route working!")
        if b'Admin Panel' in response.data:
            print("✅ Admin panel template found!")
        else:
            print("❌ Admin panel template not found")
    else:
        print(f"❌ Main route failed: {response.status_code}")
        print("Response:", response.data[:200])
    
    # Test API routes
    response = client.get('/api/pages')
    print(f"API pages status: {response.status_code}")
    if response.status_code == 200:
        print("✅ API pages route working!")
        data = response.get_json()
        if data and 'pages' in data:
            pages = data['pages']
            print(f"Found {len(pages)} pages:")
            for page_id, page_info in pages.items():
                print(f"  - {page_id}: {page_info.get('name', 'Unknown')}")
        else:
            print("❌ No pages data returned")
    else:
        print(f"❌ API pages route failed: {response.status_code}")

print("\nTest complete!")