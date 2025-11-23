import os
import json
import datetime

BASE_DIR = r'c:\Users\okakr\Downloads\new 2\kaito.com'
PAGES_JSON = r'c:\Users\okakr\Downloads\new 2\kaito.com\data\pages.json'

def get_all_pages():
    """Get all pages from pages.json"""
    if os.path.exists(PAGES_JSON):
        with open(PAGES_JSON, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def detect_new_pages():
    """Auto-detect new page folders"""
    pages = get_all_pages()
    detected_pages = []
    
    # Scan for page directories
    pages_dir = os.path.join(BASE_DIR, 'kaito.com')
    print(f"Scanning directory: {pages_dir}")
    
    if os.path.exists(pages_dir):
        for item in os.listdir(pages_dir):
            item_path = os.path.join(pages_dir, item)
            print(f"Checking item: {item} at {item_path}")
            
            if os.path.isdir(item_path) and item != 'wp-content' and item != 'wp-admin':
                print(f"Processing folder: {item}")
                
                # Try multiple strategies to find index.html
                index_file = None
                
                # Strategy 1: Direct index.html in folder
                if os.path.exists(os.path.join(item_path, 'index.html')):
                    index_file = os.path.join(item_path, 'index.html')
                    print(f"Found index.html directly: {index_file}")
                
                # Strategy 2: Look for kaito.com/index.html inside (for nested structure)
                elif os.path.exists(os.path.join(item_path, 'kaito.com', 'index.html')):
                    index_file = os.path.join(item_path, 'kaito.com', 'index.html')
                    item_path = os.path.join(item_path, 'kaito.com')  # Update path
                    print(f"Found nested index.html: {index_file}")
                
                # Strategy 3: Look for any index.html recursively (but only 1 level deep)
                else:
                    for subitem in os.listdir(item_path):
                        subitem_path = os.path.join(item_path, subitem)
                        if os.path.isdir(subitem_path):
                            sub_index = os.path.join(subitem_path, 'index.html')
                            if os.path.exists(sub_index):
                                index_file = sub_index
                                item_path = subitem_path  # Update path to the actual location
                                print(f"Found subfolder index.html: {index_file}")
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
                        print(f"✅ Detected new page: {item} at {index_file}")
                    else:
                        print(f"⏭️  Page {item} already exists")
                else:
                    print(f"❌ No index.html found for {item}")
    else:
        print(f"❌ Directory {pages_dir} does not exist")
    
    if detected_pages:
        with open(PAGES_JSON, 'w', encoding='utf-8') as f:
            json.dump(pages, f, indent=2)
        print(f"💾 Added {len(detected_pages)} new pages: {detected_pages}")
    else:
        print("📄 No new pages detected")
    
    return detected_pages

# Run detection
if __name__ == "__main__":
    print("🔍 Starting page detection...")
    detected = detect_new_pages()
    print(f"\n🏁 Detection complete. Found {len(detected)} new pages.")