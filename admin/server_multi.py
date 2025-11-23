import os, json, datetime, re, glob
from flask import Flask, request, render_template, jsonify

BASE_DIR = r'c:\\Users\\okakr\\Downloads\\new 2\\kaito.com'
UPLOAD_DIR = os.path.join(BASE_DIR, 'wp-content', 'uploads', 'custom')
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')  # Naik satu level ke data
PAGES_JSON = os.path.join(DATA_DIR, 'pages.json')

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# Initialize pages.json if not exists
if not os.path.exists(PAGES_JSON):
    default_pages = {
        "timeless": {
            "name": "Timeless Theme",
            "path": "/timeless/",
            "description": "Classic wedding invitation theme",
            "created_at": datetime.datetime.now().isoformat(),
            "last_modified": datetime.datetime.now().isoformat(),
            "content": {
                "hero_title": "WE INVITE YOU TO CELEBRATE",
                "hero_title_2": "WE INVITE YOU TO CELEBRATE",
                "couple_names": "Hanson & Catherine",
                "wedding_date": "SATURDAY, 02 MARCH 2024",
                "gallery_images": []
            }
        }
    }
    with open(PAGES_JSON, 'w', encoding='utf-8') as f:
        json.dump(default_pages, f, indent=2)

app = Flask(__name__, 
                template_folder='templates',
                static_folder='static',
                root_path=os.path.dirname(__file__))

def get_all_pages():
    """Get all available pages"""
    try:
        with open(PAGES_JSON, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def get_page_content(page_id):
    """Get content for specific page"""
    pages = get_all_pages()
    return pages.get(page_id, {}).get('content', {})

def save_page_content(page_id, content):
    """Save content for specific page"""
    pages = get_all_pages()
    if page_id in pages:
        pages[page_id]['content'].update(content)
        pages[page_id]['last_modified'] = datetime.datetime.now().isoformat()
        
        with open(PAGES_JSON, 'w', encoding='utf-8') as f:
            json.dump(pages, f, indent=2)
        return True
    return False

def detect_new_pages():
    """Auto-detect new page folders"""
    pages = get_all_pages()
    detected_pages = []
    
    # Scan for page directories
    pages_dir = os.path.join(BASE_DIR, 'kaito.com')
    if os.path.exists(pages_dir):
        for item in os.listdir(pages_dir):
            item_path = os.path.join(pages_dir, item)
            if os.path.isdir(item_path) and item != 'wp-content' and item != 'wp-admin':
                # Try multiple strategies to find index.html
                index_file = None
                
                # Strategy 1: Direct index.html in folder
                if os.path.exists(os.path.join(item_path, 'index.html')):
                    index_file = os.path.join(item_path, 'index.html')
                
                # Strategy 2: Look for kaito.com/index.html inside (for nested structure)
                elif os.path.exists(os.path.join(item_path, 'kaito.com', 'index.html')):
                    index_file = os.path.join(item_path, 'kaito.com', 'index.html')
                    item_path = os.path.join(item_path, 'kaito.com')  # Update path
                
                # Strategy 3: Look for any index.html recursively (but only 1 level deep)
                else:
                    for subitem in os.listdir(item_path):
                        subitem_path = os.path.join(item_path, subitem)
                        if os.path.isdir(subitem_path):
                            sub_index = os.path.join(subitem_path, 'index.html')
                            if os.path.exists(sub_index):
                                index_file = sub_index
                                item_path = subitem_path  # Update path to the actual location
                                break
                
                if index_file and os.path.exists(index_file):
                    page_id = item
                    if page_id not in pages:
                        # Auto-create new page
                        pages[page_id] = {
                            "name": f"{item.title()} Theme",
                            "path": f"/{item}/",
                            "description": f"Wedding invitation theme - {item}",
                            "created_at": datetime.datetime.now().isoformat(),
                            "last_modified": datetime.datetime.now().isoformat(),
                            "content": {},
                            "index_path": os.path.relpath(index_file, BASE_DIR).replace('\\', '/')
                        }
                        detected_pages.append(page_id)
                        print(f"Detected new page: {item} at {index_file}")
    
    if detected_pages:
        with open(PAGES_JSON, 'w', encoding='utf-8') as f:
            json.dump(pages, f, indent=2)
        print(f"Added {len(detected_pages)} new pages: {detected_pages}")
    
    return detected_pages

def extract_filename_from_path(path):
    """Extract filename from full path URL"""
    if not path:
        return None
    match = re.search(r'/([^/]+)$', path)
    return match.group(1) if match else None

def delete_old_background_file(old_path):
    """Delete old background file"""
    if old_path:
        filename = extract_filename_from_path(old_path)
        if filename and filename.startswith(('2025', '2024', '2023')):  # Our timestamp format
            file_path = os.path.join(UPLOAD_DIR, filename)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"Deleted old background file: {filename}")
                    return True
                except Exception as e:
                    print(f"Error deleting file {filename}: {e}")
    return False

# Multi-page routes

@app.post('/api/pages/<page_id>/content')
def save_page_content_api(page_id):
    """Save content for specific page"""
    data = request.get_json(silent=True) or request.form.to_dict(flat=True)
    
    # Handle background image uploads
    background_fields = [
        'hero_background_image', 'hero_background_video', 'background_section_1',
        'background_section_2', 'background_section_3', 'background_section_4', 
        'background_section_5', 'countdown_image', 'streaming_image',
        'prewedding_video_thumbnail', 'sticky_background_image'
    ]
    
    for field in background_fields:
        if field in request.files:
            file = request.files[field]
            if file and file.filename:
                # Delete old file if exists
                pages = get_all_pages()
                old_content = pages.get(page_id, {}).get('content', {})
                if field in old_content:
                    delete_old_background_file(old_content[field])
                
                # Save new file
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{file.filename}"
                filepath = os.path.join(UPLOAD_DIR, filename)
                file.save(filepath)
                
                # Update data with new path
                data[field] = f"/wp-content/uploads/custom/{filename}"
    
    # Save content
    if save_page_content(page_id, data):
        return jsonify({"success": True, "message": "Content saved successfully"})
    else:
        return jsonify({"success": False, "message": "Page not found"}), 404

@app.post('/api/upload-bg')
def upload_background():
    """Upload background image with page context"""
    # Get page from form data or use default
    page_id = request.form.get('page', 'timeless')
    field_name = request.form.get('field_name', 'hero_background_image')
    
    file = request.files.get('file') or request.files.get(field_name)
    if not file or not file.filename:
        return jsonify({"success": False, "message": "No file uploaded"}), 400
    
    # Delete old file if exists
    pages = get_all_pages()
    old_content = pages.get(page_id, {}).get('content', {})
    if field_name in old_content:
        delete_old_background_file(old_content[field_name])
    
    # Save new file
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{timestamp}_{file.filename}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    file.save(filepath)
    
    # Update content
    new_path = f"/wp-content/uploads/custom/{filename}"
    save_page_content(page_id, {field_name: new_path})
    
    return jsonify({"success": True, "ok": True, "url": new_path, "path": new_path})

@app.post('/api/upload')
def upload_file():
    """Upload general file with page context"""
    page_id = request.form.get('page', 'timeless')
    
    file = request.files.get('file')
    if not file or not file.filename:
        return jsonify({"success": False, "message": "No file uploaded"}), 400
    
    # Save file
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{timestamp}_{file.filename}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    file.save(filepath)
    
    new_path = f"/wp-content/uploads/custom/{filename}"
    
    return jsonify({"success": True, "ok": True, "path": new_path, "url": new_path})

@app.get('/api/pages')
def get_pages():
    """Get all available pages"""
    detect_new_pages()  # Auto-detect new pages
    pages = get_all_pages()
    return jsonify({"success": True, "pages": pages})

@app.get('/api/pages/<page_id>/content')
def get_page_content_api(page_id):
    """Get content for specific page"""
    pages = get_all_pages()
    
    if page_id not in pages:
        return jsonify({"success": False, "error": "Page not found"}), 404
    
    return jsonify({
        "success": True, 
        "content": pages[page_id].get('content', {}),
        "page_info": {
            "name": pages[page_id].get('name', page_id),
            "description": pages[page_id].get('description', ''),
            "path": pages[page_id].get('path', f'/{page_id}/')
        }
    })

@app.post('/api/content')
def update_content():
    """Update content for specific page"""
    data = request.get_json()
    
    if not data:
        return jsonify({"success": False, "error": "No data provided"}), 400
    
    page_id = data.get('page', 'timeless')
    content = data.get('content', {})
    
    pages = get_all_pages()
    
    if page_id not in pages:
        return jsonify({"success": False, "error": "Page not found"}), 404
    
    # Update page content
    if 'content' not in pages[page_id]:
        pages[page_id]['content'] = {}
    
    # Merge new content
    pages[page_id]['content'].update(content)
    pages[page_id]['last_modified'] = datetime.datetime.now().isoformat()
    
    # Save to file
    save_all_pages(pages)
    
    # Also update the actual HTML file
    page_path = os.path.join(BASE_DIR, 'kaito.com', page_id, 'index.html')
    if os.path.exists(page_path):
        # Update the HTML file with new content
        with open(page_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Update content in HTML (this is a simplified version)
        for key, value in content.items():
            if key in ['hero_title', 'greeting_text', 'guest_name_placeholder', 'apology_text', 'tombol_buka_text', 'wedding_title', 'bride_name', 'wedding_date', 'wedding_location']:
                # Update text content
                pattern = f'data-{key}="[^"]*"'
                replacement = f'data-{key}="{value}"'
                html_content = re.sub(pattern, replacement, html_content)
        
        # Save updated HTML
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    return jsonify({"success": True, "message": "Content updated successfully"})

@app.get('/')
def admin_index():
    """Admin panel with page selector"""
    detect_new_pages()  # Auto-detect new pages
    pages = get_all_pages()
    return render_template('admin.html', pages=pages)

@app.get('/api/detect-pages')
def trigger_detect_pages():
    """Manually trigger page detection"""
    detected = detect_new_pages()
    return jsonify({
        "success": True, 
        "detected_pages": detected,
        "total_pages": len(get_all_pages())
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)