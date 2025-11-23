#!/usr/bin/env python3

from flask import Flask, render_template, jsonify, request
from datetime import datetime
import json
import os
import sys
import requests

# Tambahkan path untuk import
sys.path.append(os.path.dirname(__file__))

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')

@app.route('/')
def index():
    """Simple test page"""
    pages = {
        'timeless': {'name': 'Timeless Theme'},
        'elegant': {'name': 'Elegant Theme'}
    }
    return render_template('admin.html', pages=pages)

@app.route('/api/pages')
def get_pages():
    """Get all pages"""
    return jsonify({
        "success": True,
        "pages": {
            'timeless': {'name': 'Timeless Theme'},
            'elegant': {'name': 'Elegant Theme'}
        }
    })

@app.route('/api/pages/<page_id>/content')
def get_page_content(page_id):
    """Get content for specific page"""
    if page_id == 'elegant':
        # Load content from pages.json
        try:
            pages_file = os.path.join('..', 'data', 'pages.json')
            with open(pages_file, 'r') as f:
                pages_data = json.load(f)
            
            elegant_content = pages_data.get('elegant', {}).get('content', {})
            
            return jsonify({
                "success": True,
                "content": elegant_content,
                "page_info": {
                    "name": "Elegant Theme - Jimmy & Sherly",
                    "description": "Jimmy & Sherly Wedding Invitation",
                    "path": "http://localhost:5002/editable",
                    "editable": True,
                    "theme": "elegant",
                    "external_link": "http://localhost:5002/editable",
                    "server_port": 5002
                }
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "message": f"Error loading elegant content: {str(e)}"
            })
    
    # Default content for timeless
    content = {
        'hero_title': 'WE INVITE YOU TO CELEBRATE',
        'hero_title_2': 'WE INVITE YOU TO CELEBRATE',
        'couple_names': 'Hanson & Catherine',
        'wedding_date': 'SATURDAY, 02 MARCH 2024',
        'gallery_images': []
    }
    
    return jsonify({
        "success": True,
        "content": content,
        "page_info": {
            "name": f"{page_id.title()} Theme",
            "description": f"Wedding invitation theme - {page_id}",
            "path": f"/{page_id}/"
        }
    })

@app.route('/elegant_editable.html')
def serve_elegant_editable():
    """Serve the editable elegant HTML file with dynamic content"""
    try:
        # Load content from pages.json
        pages_file = os.path.join('..', 'data', 'pages.json')
        with open(pages_file, 'r') as f:
            pages_data = json.load(f)
        
        content = pages_data.get('elegant', {}).get('content', {})
        
        # Read the template file - located in kaito.com directory
        template_file = os.path.join('..', 'kaito.com', 'elegant_editable.html')
        with open(template_file, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Simple template replacement (since we can't use Jinja2 easily)
        # Replace template variables with actual content
        for key, value in content.items():
            placeholder = '{{ content.get(\'' + key + '\', \'\') }}'
            if placeholder in template_content:
                template_content = template_content.replace(placeholder, str(value))
        
        # Handle the |safe filter for HTML content
        template_content = template_content.replace('|safe', '')
        
        return template_content, 200, {'Content-Type': 'text/html; charset=utf-8'}
        
    except Exception as e:
        return f"Error serving elegant page: {str(e)}", 500

@app.route('/api/upload', methods=['POST'])
def handle_upload():
    """Handle file uploads for elegant page"""
    try:
        # Check if this is elegant upload
        if request.form.get('page') == 'elegant':
            # Forward to elegant server
            try:
                # Get the file and field name
                files = request.files
                field_name = request.form.get('field_name')
                
                if not files or not field_name:
                    return jsonify({"ok": False, "message": "No files or field name provided"})
                
                # Forward to elegant server
                response = requests.post('http://localhost:5002/api/upload', 
                                         files=files,
                                         data={'page': 'elegant', 'field_name': field_name})
                return jsonify(response.json())
                
            except Exception as e:
                return jsonify({"ok": False, "message": f"Error connecting to elegant server: {str(e)}"})
        
        # Handle other pages upload here if needed
        return jsonify({"ok": False, "message": "Upload not supported for this page"})
        
    except Exception as e:
        return jsonify({"ok": False, "message": f"Upload error: {str(e)}"})

@app.route('/api/content', methods=['POST'])
def save_content():
    """Save content for specific page"""
    try:
        data = request.get_json()
        page = data.get('page')
        content = data.get('content')
        
        if not page or not content:
            return jsonify({"success": False, "message": "Missing page or content"})
        
        # For elegant, forward to port 5002
        if page == 'elegant':
            try:
                response = requests.post('http://localhost:5002/api/content', 
                                         json={'content': content},
                                         headers={'Content-Type': 'application/json'})
                return jsonify(response.json())
            except Exception as e:
                return jsonify({"success": False, "message": f"Error connecting to elegant server: {str(e)}"})
        
        # Read current pages.json
        pages_file = os.path.join('..', 'data', 'pages.json')
        with open(pages_file, 'r') as f:
            pages_data = json.load(f)
        
        # Update content for the specific page
        if page in pages_data:
            pages_data[page]['content'].update(content)
            pages_data[page]['last_modified'] = datetime.now().isoformat()
            
            # Write back to file
            with open(pages_file, 'w') as f:
                json.dump(pages_data, f, indent=2)
            
            return jsonify({"success": True, "message": "Content saved successfully"})
        else:
            return jsonify({"success": False, "message": "Page not found"})
            
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

if __name__ == '__main__':
    print("Starting simple server...")
    print(f"Template folder: {app.template_folder}")
    print(f"Running on http://localhost:5001")
    app.run(debug=True, port=5001, host='0.0.0.0')