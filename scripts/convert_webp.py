import os
import json
from PIL import Image

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
JSON_PATH = os.path.join(BASE, 'data', 'pages.json')
KAITO_ROOT = os.path.join(BASE, 'kaito.com')

def to_abs(rel):
    rel = rel.lstrip('/')
    return os.path.join(KAITO_ROOT, rel.replace('/', os.sep))

def to_rel(abs_path):
    return '/' + os.path.relpath(abs_path, KAITO_ROOT).replace(os.sep, '/')

def convert_to_webp(abs_path, quality=80):
    root, _ = os.path.splitext(abs_path)
    out = root + '.webp'
    im = Image.open(abs_path).convert('RGB')
    im.save(out, 'WEBP', quality=quality, method=6)
    return out

def run():
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    timeless = data.get('timeless', {})
    content = timeless.get('content', {})

    keys_single = [
        'hero_image', 'background_section_4', 'streaming_image',
        'prewedding_video_thumbnail', 'sticky_background_image'
    ]
    keys_list = ['gallery_images']

    converted = []
    for k in keys_single:
        p = content.get(k)
        if isinstance(p, str) and p.lower().endswith(('.jpg', '.jpeg')):
            abs_p = to_abs(p)
            if os.path.exists(abs_p):
                out = convert_to_webp(abs_p)
                content[k] = to_rel(out)
                converted.append(abs_p)

    for k in keys_list:
        arr = content.get(k, [])
        new_arr = []
        for p in arr:
            if isinstance(p, str) and p.lower().endswith(('.jpg', '.jpeg')):
                abs_p = to_abs(p)
                if os.path.exists(abs_p):
                    out = convert_to_webp(abs_p)
                    new_arr.append(to_rel(out))
                    converted.append(abs_p)
                else:
                    new_arr.append(p)
            else:
                new_arr.append(p)
        content[k] = new_arr

    timeless['content'] = content
    data['timeless'] = timeless

    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Converted {len(converted)} images to WebP")

if __name__ == '__main__':
    run()
