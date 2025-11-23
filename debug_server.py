#!/usr/bin/env python3

import sys
import os
sys.path.append('admin')

# Test the Flask app dengan debug
from server_multi import app

print("=== FLASK APP DEBUG ===")
print(f"Template folder: {app.template_folder}")
print(f"Root path: {app.root_path}")
print(f"Static folder: {app.static_folder}")

# Test dengan test client
print("\n=== TEST CLIENT ===")
with app.test_client() as client:
    response = client.get('/')
    print(f"Test client status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Test client berhasil")
    else:
        print("❌ Test client gagal")

# Test dengan real server check
print("\n=== REAL SERVER CHECK ===")
try:
    import requests
    response = requests.get('http://localhost:5000/', timeout=2)
    print(f"Real server status: {response.status_code}")
except Exception as e:
    print(f"Real server error: {e}")

print("\n=== TEMPLATE CHECK ===")
template_path = os.path.join(os.path.dirname(__file__), 'admin', 'templates', 'admin.html')
print(f"Template path: {template_path}")
print(f"Template exists: {os.path.exists(template_path)}")