#!/usr/bin/env python3

from flask import Flask, send_from_directory, send_file, jsonify, request
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime

app = Flask(__name__)

# Path ke folder elegant (sebelumnya kaito2)
KAITO2_BASE = r'c:\Users\okakr\Downloads\new 2\kaito.com\kaito.com\elegant\kaito.com'
PAGES_FILE = r'c:\Users\okakr\Downloads\new 2\kaito.com\data\pages.json'

@app.route('/')
def index():
    """Serve elegant index.html (sebelumnya kaito2)"""
    return send_file(os.path.join(KAITO2_BASE, 'index.html'))

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files (CSS, JS, images, etc.)"""
    return send_from_directory(KAITO2_BASE, filename)

@app.route('/wp-content/<path:filename>')
def serve_wp_content(filename):
    """Serve WordPress content files"""
    return send_from_directory(os.path.join(KAITO2_BASE, 'wp-content'), filename)

@app.route('/wp-includes/<path:filename>')
def serve_wp_includes(filename):
    """Serve WordPress includes files"""
    return send_from_directory(os.path.join(KAITO2_BASE, 'wp-includes'), filename)

@app.route('/wp-admin/<path:filename>')
def serve_wp_admin(filename):
    """Serve WordPress admin files"""
    return send_from_directory(os.path.join(KAITO2_BASE, 'wp-admin'), filename)

@app.route('/api/info')
def get_info():
    """Get info about elegant page (sebelumnya kaito2)"""
    return jsonify({
        "success": True,
        "page": "elegant",
        "title": "THE WEDDING OF Jimmy & Sherly",
        "description": "Jimmy & Sherly Wedding Invitation",
        "base_path": KAITO2_BASE
    })

@app.route('/editable')
def editable_index():
    """Serve editable version of elegant with dynamic content (sebelumnya kaito2)"""
    try:
        # Load content from pages.json
        if os.path.exists(PAGES_FILE):
            with open(PAGES_FILE, 'r', encoding='utf-8') as f:
                pages_data = json.load(f)
            content = pages_data.get('elegant', {}).get('content', {})
        else:
            content = {}
        
        # Read the original index.html
        with open(os.path.join(KAITO2_BASE, 'index.html'), 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Comprehensive content replacement
        replacements = {
            # Basic info
            'Jimmy &amp; Sherly': content.get('couple_names', 'Jimmy & Sherly'),
            'THE WEDDING OF Jimmy &amp; Sherly': content.get('page_title', 'THE WEDDING OF Jimmy & Sherly'),
            'Jimmy & Sherly': content.get('couple_names', 'Jimmy & Sherly'),
            'SATURDAY, 21 AUGUST 2023': content.get('wedding_date', 'SATURDAY, 21 AUGUST 2023'),
            'save the date': content.get('open_button', 'save the date'),
            'Save the date': content.get('open_button', 'Save the date'),
            
            # Couple details
            'Jimmy': content.get('groom_name', 'Jimmy'),
            'Sherly': content.get('bride_name', 'Sherly'),
            'The Groom': content.get('groom_role', 'The Groom'),
            'The Bride': content.get('bride_role', 'The Bride'),
            'Son of Mr. & Mrs. Anderson': content.get('groom_parents', 'Son of Mr. & Mrs. Anderson'),
            'Daughter of Mr. & Mrs. Williams': content.get('bride_parents', 'Daughter of Mr. & Mrs. Williams'),
            
            # Event details
            'Wedding Ceremony': content.get('ceremony_title', 'Wedding Ceremony'),
            'Saturday, August 21, 2023': content.get('ceremony_date', 'Saturday, August 21, 2023'),
            '10:00 AM - 12:00 PM': content.get('ceremony_time', '10:00 AM - 12:00 PM'),
            'St. Mary\'s Catholic Church<br>123 Wedding Avenue<br>Downtown District': content.get('ceremony_location', 'St. Mary\'s Catholic Church<br>123 Wedding Avenue<br>Downtown District'),
            
            'Wedding Reception': content.get('reception_title', 'Wedding Reception'),
            '6:00 PM - 10:00 PM': content.get('reception_time', '6:00 PM - 10:00 PM'),
            'Grand Ballroom Hotel<br>456 Celebration Street<br>City Center': content.get('reception_location', 'Grand Ballroom Hotel<br>456 Celebration Street<br>City Center'),
            
            # Form labels
            'Your Name': content.get('form_name_label', 'Your Name'),
            'Email Address': content.get('form_email_label', 'Email Address'),
            'Number of Guests': content.get('form_guests_label', 'Number of Guests'),
            'Message (Optional)': content.get('form_message_label', 'Message (Optional)'),
            'Send RSVP': content.get('form_submit_button', 'Send RSVP'),
            
            # Footer
            'With love and gratitude,': content.get('footer_text', 'With love and gratitude,'),
            '📷 Instagram': content.get('instagram_link', '📷 Instagram'),
            '📘 Facebook': content.get('facebook_link', '📘 Facebook'),
            
            # Section titles
            'The Couple': content.get('couple_section_title', 'The Couple'),
            'Wedding Events': content.get('event_section_title', 'Wedding Events'),
            'Our Gallery': content.get('gallery_section_title', 'Our Gallery'),
            'RSVP': content.get('rsvp_section_title', 'RSVP'),
            'We would love to celebrate with you! Please let us know if you can join us on our special day.': content.get('rsvp_description', 'We would love to celebrate with you! Please let us know if you can join us on our special day.')
        }
        
        # Apply all replacements
        for old_text, new_text in replacements.items():
            html_content = html_content.replace(old_text, new_text)

        # Replace background slideshow images (Elementor) using gallery_image_1..3
        # Support both absolute and local relative URLs found in the original HTML
        gallery_1 = content.get('gallery_image_1', '/wp-content/uploads/2024/07/Foto-SLide-Gallery-1-Large-SHERLY-1-1.jpeg')
        gallery_2 = content.get('gallery_image_2', '/wp-content/uploads/2024/07/Foto-Slide-Gallery-15-Large-SHERLY.jpeg')
        gallery_3 = content.get('gallery_image_3', '/wp-content/uploads/2024/07/Fotno-Slide-Hitungan-Hari-2-Large-SHERLY-1.jpeg')
        cover_bg = content.get('cover_background', '/wp-content/uploads/2024/07/Fotno-Slide-Hitungan-Hari-2-Large-SHERLY-1.jpeg')

        image_replacements = [
            # Cover background
            ('/wp-content/uploads/2024/07/Fotno-Slide-Hitungan-Hari-2-Large-SHERLY-1.jpeg', cover_bg),
            
            # Slide 1 variants
            ('https://groovepublic.com/wp-content/uploads/2024/07/Foto-SLide-Gallery-1-Large-SHERLY-1-1.jpeg', gallery_1),
            ('/wp-content/uploads/2024/07/Foto-SLide-Gallery-1-Large-SHERLY-1-1.jpeg', gallery_1),
            ('https://groovepublic.com/wp-content/uploads/2024/07/Foto-SLide-Gallery-1-Large-SHERLY.jpeg', gallery_1),
            ('/wp-content/uploads/2024/07/Foto-SLide-Gallery-1-Large-SHERLY.jpeg', gallery_1),

            # Slide 2 variants
            ('https://groovepublic.com/wp-content/uploads/2024/07/Foto-Slide-Gallery-15-Large-SHERLY.jpeg', gallery_2),
            ('/wp-content/uploads/2024/07/Foto-Slide-Gallery-15-Large-SHERLY.jpeg', gallery_2),

            # Slide 3 variants
            ('https://groovepublic.com/wp-content/uploads/2024/07/Fotno-Slide-Hitungan-Hari-2-Large-SHERLY-1.jpeg', gallery_3),
            ('/wp-content/uploads/2024/07/Fotno-Slide-Hitungan-Hari-2-Large-SHERLY-1.jpeg', gallery_3),
            ('https://groovepublic.com/wp-content/uploads/2024/07/Foto-Slide-Hitungan-Hari-2-Large-SHERLY.jpeg', gallery_3),
            ('/wp-content/uploads/2024/07/Foto-Slide-Hitungan-Hari-2-Large-SHERLY.jpeg', gallery_3),
        ]

        for old_url, new_url in image_replacements:
            if new_url:
                html_content = html_content.replace(old_url, new_url)

        # Add data attributes for editing to key elements
        html_content = html_content.replace(
            '<title>THE WEDDING OF Jimmy &amp; Sherly</title>',
            f'<title data-editable="true" data-key="page_title">{content.get("page_title", "THE WEDDING OF Jimmy & Sherly")}</title>'
        )
        
        # Add API endpoint script for saving clicked background images
        api_script = '''
        <script>
        // Save background image that was clicked and changed
        function saveBackgroundImage(imageUrl, fieldName) {
            fetch('/api/content', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    [fieldName]: imageUrl
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log(`Background image saved: ${fieldName} = ${imageUrl}`);
                } else {
                    console.error('Failed to save background image');
                }
            })
            .catch(error => {
                console.error('Error saving background image:', error);
            });
        }
        
        // Override the makeImagesEditable function to add auto-save
        if (typeof makeImagesEditable === 'function') {
            const originalFunction = makeImagesEditable;
            makeImagesEditable = function() {
                originalFunction();
                
                // Add auto-save for background changes
                const coverSection = document.querySelector('.cover-section');
                if (coverSection) {
                    const originalClickHandler = coverSection.onclick;
                    coverSection.onclick = function() {
                        const currentBg = this.style.backgroundImage || window.getComputedStyle(this).backgroundImage;
                        const currentImage = currentBg.replace(/url\(["']?([^"']*)["']?\).*/i, '$1');
                        
                        const newImage = prompt('Masukkan URL gambar baru untuk background:', currentImage);
                        if (newImage && newImage !== currentImage) {
                            this.style.backgroundImage = `linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), url("${newImage}")`;
                            saveBackgroundImage(newImage, 'cover_background');
                            alert('✅ Background berhasil diubah dan disimpan!');
                        }
                    };
                }
                
                // Add auto-save for gallery images
                document.querySelectorAll('.gallery-item img').forEach(img => {
                    const originalClickHandler = img.onclick;
                    img.onclick = function(e) {
                        e.stopPropagation();
                        const currentSrc = this.src;
                        const newSrc = prompt('Masukkan URL gambar baru:', currentSrc);
                        if (newSrc && newSrc !== currentSrc) {
                            this.src = newSrc;
                            
                            // Determine which gallery image this is
                            const galleryItem = this.closest('.gallery-item');
                            const galleryItems = Array.from(document.querySelectorAll('.gallery-item'));
                            const index = galleryItems.indexOf(galleryItem) + 1;
                            
                            saveBackgroundImage(newSrc, `gallery_image_${index}`);
                            alert('✅ Gambar gallery berhasil diubah dan disimpan!');
                        }
                    };
                });
            };
        }
        </script>
        '''
        
        # Insert the API script before closing body tag
        html_content = html_content.replace('</body>', api_script + '</body>')
        
        return html_content, 200, {'Content-Type': 'text/html; charset=utf-8'}
        
    except Exception as e:
        return f"Error serving editable page: {str(e)}", 500

@app.route('/api/upload', methods=['POST'])
def handle_upload():
    """Handle file uploads for elegant page"""
    try:
        if 'cover_background' in request.files:
            file = request.files['cover_background']
            if file and file.filename:
                # Get original filename with extension
                original_filename = file.filename
                filename = secure_filename(original_filename)
                
                # If secure_filename removed extension, add it back
                if '.' not in filename and '.' in original_filename:
                    ext = original_filename.rsplit('.', 1)[1].lower()
                    filename = f"{filename}.{ext}"
                
                upload_folder = os.path.join('kaito.com', 'wp-content', 'uploads', '2024', '07')
                os.makedirs(upload_folder, exist_ok=True)
                
                filepath = os.path.join(upload_folder, filename)
                file.save(filepath)
                
                # Return relative path
                relative_path = f'/wp-content/uploads/2024/07/{filename}'
                
                # Update pages.json
                if os.path.exists(PAGES_FILE):
                    with open(PAGES_FILE, 'r', encoding='utf-8') as f:
                        pages_data = json.load(f)
                else:
                    pages_data = {}
                
                if 'elegant' not in pages_data:
                    pages_data['elegant'] = {'content': {}}
                elif 'content' not in pages_data['elegant']:
                    pages_data['elegant']['content'] = {}
                
                pages_data['elegant']['content']['cover_background'] = relative_path
                
                with open(PAGES_FILE, 'w', encoding='utf-8') as f:
                    json.dump(pages_data, f, indent=2, ensure_ascii=False)
                
                return jsonify({"ok": True, "path": relative_path, "message": "Background uploaded successfully"})
        
        elif 'gallery_image_1' in request.files:
            file = request.files['gallery_image_1']
            if file and file.filename:
                # Get original filename with extension
                original_filename = file.filename
                filename = secure_filename(original_filename)
                
                # If secure_filename removed extension, add it back
                if '.' not in filename and '.' in original_filename:
                    ext = original_filename.rsplit('.', 1)[1].lower()
                    filename = f"{filename}.{ext}"
                
                upload_folder = os.path.join('kaito.com', 'wp-content', 'uploads', '2024', '07')
                os.makedirs(upload_folder, exist_ok=True)
                
                filepath = os.path.join(upload_folder, filename)
                file.save(filepath)
                
                relative_path = f'/wp-content/uploads/2024/07/{filename}'
                
                # Update pages.json
                if os.path.exists(PAGES_FILE):
                    with open(PAGES_FILE, 'r', encoding='utf-8') as f:
                        pages_data = json.load(f)
                else:
                    pages_data = {}
                
                if 'elegant' not in pages_data:
                    pages_data['elegant'] = {'content': {}}
                elif 'content' not in pages_data['elegant']:
                    pages_data['elegant']['content'] = {}
                
                pages_data['elegant']['content']['gallery_image_1'] = relative_path
                
                with open(PAGES_FILE, 'w', encoding='utf-8') as f:
                    json.dump(pages_data, f, indent=2, ensure_ascii=False)
                
                return jsonify({"ok": True, "path": relative_path, "message": "Gallery image 1 uploaded successfully"})
        
        elif 'gallery_image_2' in request.files:
            file = request.files['gallery_image_2']
            if file and file.filename:
                # Get original filename with extension
                original_filename = file.filename
                filename = secure_filename(original_filename)
                
                # If secure_filename removed extension, add it back
                if '.' not in filename and '.' in original_filename:
                    ext = original_filename.rsplit('.', 1)[1].lower()
                    filename = f"{filename}.{ext}"
                
                upload_folder = os.path.join('kaito.com', 'wp-content', 'uploads', '2024', '07')
                os.makedirs(upload_folder, exist_ok=True)
                
                filepath = os.path.join(upload_folder, filename)
                file.save(filepath)
                
                relative_path = f'/wp-content/uploads/2024/07/{filename}'
                
                # Update pages.json
                if os.path.exists(PAGES_FILE):
                    with open(PAGES_FILE, 'r', encoding='utf-8') as f:
                        pages_data = json.load(f)
                else:
                    pages_data = {}
                
                if 'elegant' not in pages_data:
                    pages_data['elegant'] = {'content': {}}
                elif 'content' not in pages_data['elegant']:
                    pages_data['elegant']['content'] = {}
                
                pages_data['elegant']['content']['gallery_image_2'] = relative_path
                
                with open(PAGES_FILE, 'w', encoding='utf-8') as f:
                    json.dump(pages_data, f, indent=2, ensure_ascii=False)
                
                return jsonify({"ok": True, "path": relative_path, "message": "Gallery image 2 uploaded successfully"})
        
        elif 'gallery_image_3' in request.files:
            file = request.files['gallery_image_3']
            if file and file.filename:
                # Get original filename with extension
                original_filename = file.filename
                filename = secure_filename(original_filename)
                
                # If secure_filename removed extension, add it back
                if '.' not in filename and '.' in original_filename:
                    ext = original_filename.rsplit('.', 1)[1].lower()
                    filename = f"{filename}.{ext}"
                
                upload_folder = os.path.join('kaito.com', 'wp-content', 'uploads', '2024', '07')
                os.makedirs(upload_folder, exist_ok=True)
                
                filepath = os.path.join(upload_folder, filename)
                file.save(filepath)
                
                relative_path = f'/wp-content/uploads/2024/07/{filename}'
                
                # Update pages.json
                if os.path.exists(PAGES_FILE):
                    with open(PAGES_FILE, 'r', encoding='utf-8') as f:
                        pages_data = json.load(f)
                else:
                    pages_data = {}
                
                if 'elegant' not in pages_data:
                    pages_data['elegant'] = {'content': {}}
                elif 'content' not in pages_data['elegant']:
                    pages_data['elegant']['content'] = {}
                
                pages_data['elegant']['content']['gallery_image_3'] = relative_path
                
                with open(PAGES_FILE, 'w', encoding='utf-8') as f:
                    json.dump(pages_data, f, indent=2, ensure_ascii=False)
                
                return jsonify({"ok": True, "path": relative_path, "message": "Gallery image 3 uploaded successfully"})
        
        return jsonify({"ok": False, "message": "No valid file field found"})
        
    except Exception as e:
        return jsonify({"ok": False, "message": f"Upload error: {str(e)}"})

@app.route('/api/content', methods=['GET', 'POST'])
def handle_content():
    """Get or save content for elegant (sebelumnya kaito2)"""
    if request.method == 'GET':
        try:
            if os.path.exists(PAGES_FILE):
                with open(PAGES_FILE, 'r', encoding='utf-8') as f:
                    pages_data = json.load(f)
                content = pages_data.get('elegant', {}).get('content', {})
            else:
                content = {}
            
            return jsonify({
                "success": True,
                "content": content,
                "page_info": {
                    "name": "Elegant - Jimmy & Sherly",
                    "description": "Jimmy & Sherly Wedding Invitation",
                    "editable": True
                }
            })
        except Exception as e:
            return jsonify({"success": False, "message": str(e)})
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            content = data.get('content', {})
            
            # Load existing pages data
            if os.path.exists(PAGES_FILE):
                with open(PAGES_FILE, 'r', encoding='utf-8') as f:
                    pages_data = json.load(f)
            else:
                pages_data = {}
            
            # Update elegant content (sebelumnya kaito2) - merge dengan existing data
            if 'elegant' not in pages_data:
                pages_data['elegant'] = {}
            
            # Merge dengan existing content, jangan replace seluruhnya
            existing_content = pages_data['elegant'].get('content', {})
            merged_content = {**existing_content, **content}  # Merge dictionaries
            pages_data['elegant']['content'] = merged_content
            pages_data['elegant']['last_modified'] = datetime.now().isoformat()
            
            # Save back to file
            with open(PAGES_FILE, 'w', encoding='utf-8') as f:
                json.dump(pages_data, f, indent=2, ensure_ascii=False)
            
            return jsonify({"success": True, "message": "Content saved successfully"})
            
        except Exception as e:
            return jsonify({"success": False, "message": str(e)})

if __name__ == '__main__':
    print("🎉 Starting Elegant Wedding Server... (sebelumnya Kaito2)")
    print(f"📁 Serving files from: {KAITO2_BASE}")
    print("🌐 Access at: http://localhost:5002")
    print("💍 Jimmy & Sherly Wedding Invitation")
    app.run(debug=True, port=5002, host='0.0.0.0')