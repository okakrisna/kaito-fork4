#!/usr/bin/env python3

import sys
import os
sys.path.append('admin')

# Debug Flask routes
from server_multi import app

print("=== FLASK ROUTES ===")
for rule in app.url_map.iter_rules():
    print(f"Path: {rule.rule} -> Endpoint: {rule.endpoint}")

print("\n=== FLASK CONFIG ===")
print(f"Template folder: {app.template_folder}")
print(f"Static folder: {app.static_folder}")
print(f"Root path: {app.root_path}")

# Test semua routes
print("\n=== ROUTE TESTING ===")
with app.test_client() as client:
    routes = ['/', '/api/pages', '/api/detect-pages']
    for route in routes:
        response = client.get(route)
        print(f"{route}: {response.status_code}")
        if response.status_code != 200:
            print(f"  Error response: {response.data[:100]}")