import os, json, datetime, re
from flask import Flask, request, render_template, jsonify

BASE_DIR = r'c:\Users\okakr\Downloads\new 2\kaito.com\kaito.com'
UPLOAD_DIR = os.path.join(BASE_DIR, 'wp-content', 'uploads', 'custom')
DATA_DIR = os.path.join(BASE_DIR, 'data')
CONTENT_JSON = os.path.join(DATA_DIR, 'content.json')

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(CONTENT_JSON):
    with open(CONTENT_JSON, 'w', encoding='utf-8') as f:
        json.dump({"hero_title":"WE INVITE YOU TO CELEBRATE","background_video":"./timeless/assets/backgroundvideo.test.mp4","gallery_images":[]}, f)

app = Flask(__name__, template_folder='templates')

@app.get('/api/content')
def get_content():
    with open(CONTENT_JSON, 'r', encoding='utf-8') as f:
        return jsonify(json.load(f))

def extract_filename_from_path(path):
    """Extract filename from full path URL"""
    if not path:
        return None
    # Handle URLs like /wp-content/uploads/custom/20241118_123456_oldfile.jpg
    match = re.search(r'/([^/]+)$', path)
    return match.group(1) if match else None

def delete_old_background_file(old_path):
    """Delete old background image file from server"""
    if not old_path:
        return
    
    filename = extract_filename_from_path(old_path)
    if not filename:
        return
    
    # Try to delete from custom upload directory
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"Deleted old background file: {filename}")
            return True
        except Exception as e:
            print(f"Error deleting file {filename}: {e}")
    
    return False

@app.post('/api/content')
def save_content():
    data = request.get_json(silent=True) or request.form.to_dict(flat=True)
    with open(CONTENT_JSON, 'r', encoding='utf-8') as f:
        current = json.load(f)
    
    # Check for background image changes and delete old files
    background_fields = [
        'background_section_1', 'background_section_2', 'background_section_3', 
        'background_section_4', 'background_section_5', 'countdown_image', 'streaming_image'
    ]
    
    for field in background_fields:
        if field in data and data[field] and data[field] != current.get(field):
            # New background is different from old one, delete old file
            old_path = current.get(field)
            if old_path and old_path != data[field]:
                delete_old_background_file(old_path)
    
    current.update({k:v for k,v in data.items() if v is not None and v != ''})
    with open(CONTENT_JSON, 'w', encoding='utf-8') as f:
        json.dump(current, f)
    return jsonify({"ok": True, "content": current})

@app.post('/api/upload')
def upload():
    file = request.files.get('file')
    if not file:
        return jsonify({"ok": False, "error": "no file"}), 400
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    name = ts + '_' + file.filename
    path = os.path.join(UPLOAD_DIR, name)
    file.save(path)
    rel = '/wp-content/uploads/custom/' + name
    return jsonify({"ok": True, "path": rel})

@app.post('/api/upload-bg')
def upload_bg():
    """Upload background images with automatic old file cleanup"""
    file = request.files.get('hero_background_image') or request.files.get('hero_background_video') or request.files.get('background_section_2') or request.files.get('background_section_3') or request.files.get('countdown_image') or request.files.get('streaming_image')
    if not file:
        return jsonify({"ok": False, "error": "no file"}), 400
    
    # Load current content to check for old files
    with open(CONTENT_JSON, 'r', encoding='utf-8') as f:
        current = json.load(f)
    
    # Determine field type and old file path
    if 'hero_background_image' in request.files:
        field_name = 'hero_background_image'
        old_path = current.get('hero_background_image', '')
        # Also update background_section_1 for consistency
        section_field = 'background_section_1'
        old_section_path = current.get('background_section_1', '')
    elif 'hero_background_video' in request.files:
        field_name = 'hero_background_video'
        old_path = current.get('hero_background_video', '')
        section_field = None  # No section equivalent for video
    elif 'background_section_2' in request.files:
        field_name = 'background_section_2'
        old_path = current.get('background_section_2', '')
        section_field = None  # No section equivalent for groom background
    elif 'background_section_3' in request.files:
        field_name = 'background_section_3'
        old_path = current.get('background_section_3', '')
        section_field = None  # No section equivalent for bride background
    elif 'countdown_image' in request.files:
        field_name = 'countdown_image'
        old_path = current.get('countdown_image', '')
        section_field = None  # No section equivalent for countdown image
    elif 'streaming_image' in request.files:
        field_name = 'streaming_image'
        old_path = current.get('streaming_image', '')
        section_field = None  # No section equivalent for streaming background
    else:
        return jsonify({"ok": False, "error": "unknown field"}), 400
    
    # Delete old files if exists
    if old_path:
        delete_old_background_file(old_path)
    if 'hero_background_image' in request.files and old_section_path:
        delete_old_background_file(old_section_path)
    
    # Save new file
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    name = ts + '_' + file.filename
    path = os.path.join(UPLOAD_DIR, name)
    file.save(path)
    rel = '/wp-content/uploads/custom/' + name
    
    # Update content.json
    current[field_name] = rel
    if 'hero_background_image' in request.files:
        current[section_field] = rel  # Also update background_section_1
    with open(CONTENT_JSON, 'w', encoding='utf-8') as f:
        json.dump(current, f)
    
    return jsonify({"ok": True, "url": rel})

@app.get('/admin')
def admin():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)