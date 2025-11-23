#!/usr/bin/env python3

from flask import Flask, render_template_string, jsonify
import json
import os

app = Flask(__name__)

def load_page_content():
    """Load kaito2 content from pages.json"""
    try:
        pages_file = os.path.join('data', 'pages.json')
        with open(pages_file, 'r') as f:
            pages_data = json.load(f)
        return pages_data.get('kaito2', {}).get('content', {})
    except Exception as e:
        print(f"Error loading content: {e}")
        return {}

@app.route('/')
def index():
    """Serve the editable kaito2 HTML with dynamic content"""
    content = load_page_content()
    
    html_template = '''<!DOCTYPE html>
<html lang="en-US">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ content.get('page_title', 'THE WEDDING OF Jimmy & Sherly') }}</title>
    <meta name="description" content="{{ content.get('meta_description', 'Invitation') }}">
    
    <!-- Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Hanken+Grotesk:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- AOS Animation -->
    <link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">
    <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
    
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Hanken Grotesk', sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f8f8f8;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        /* Cover Section */
        .cover-section {
            min-height: 100vh;
            background: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), 
                        url('{{ content.get('gallery_image_3', '/wp-content/uploads/2024/07/Fotno-Slide-Hitungan-Hari-2-Large-SHERLY-1.jpeg') }}') center/cover;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            color: white;
            position: relative;
        }
        
        .cover-content h3 {
            font-family: 'Playfair Display', serif;
            font-size: 2.5rem;
            margin-bottom: 1rem;
            font-weight: 300;
        }
        
        .cover-content h1 {
            font-family: 'Playfair Display', serif;
            font-size: 4rem;
            margin-bottom: 2rem;
            font-weight: 700;
        }
        
        .cover-content .date {
            font-size: 1.2rem;
            margin-bottom: 3rem;
            letter-spacing: 2px;
        }
        
        .btn-open {
            background: rgba(255,255,255,0.2);
            border: 2px solid white;
            color: white;
            padding: 15px 30px;
            font-size: 1.1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }
        
        .btn-open:hover {
            background: white;
            color: #333;
        }
        
        /* Couple Section */
        .couple-section {
            padding: 80px 0;
            background: #f6f6f4;
            text-align: center;
        }
        
        .section-title {
            font-family: 'Playfair Display', serif;
            font-size: 3rem;
            margin-bottom: 3rem;
            color: #333;
        }
        
        .couple-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 60px;
            max-width: 1000px;
            margin: 0 auto;
        }
        
        .couple-member {
            text-align: center;
        }
        
        .couple-member h3 {
            font-family: 'Playfair Display', serif;
            font-size: 2rem;
            margin-bottom: 1rem;
            color: #333;
        }
        
        .couple-member .role {
            font-size: 1.1rem;
            color: #666;
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .couple-member p {
            font-size: 1rem;
            color: #666;
            line-height: 1.8;
            margin-bottom: 1rem;
        }
        
        .couple-member .parent-names {
            font-style: italic;
            color: #888;
            margin-top: 1rem;
        }
        
        /* Event Details Section */
        .event-section {
            padding: 80px 0;
            background: white;
            text-align: center;
        }
        
        .event-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
            max-width: 1000px;
            margin: 0 auto;
        }
        
        .event-card {
            background: #f8f8f8;
            padding: 40px;
            border-radius: 10px;
        }
        
        .event-card h3 {
            font-family: 'Playfair Display', serif;
            font-size: 1.8rem;
            margin-bottom: 1rem;
            color: #333;
        }
        
        .event-card .date {
            font-size: 1.2rem;
            color: #666;
            margin-bottom: 0.5rem;
            font-weight: 600;
        }
        
        .event-card .time {
            font-size: 1.1rem;
            color: #888;
            margin-bottom: 1rem;
        }
        
        .event-card .location {
            font-size: 1rem;
            color: #666;
            line-height: 1.6;
        }
        
        /* Gallery Section */
        .gallery-section {
            padding: 80px 0;
            background: #f6f6f4;
            text-align: center;
        }
        
        .gallery-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .gallery-item {
            position: relative;
            overflow: hidden;
            border-radius: 10px;
            height: 400px;
        }
        
        .gallery-item img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s ease;
        }
        
        .gallery-item:hover img {
            transform: scale(1.05);
        }
        
        /* RSVP Section */
        .rsvp-section {
            padding: 80px 0;
            background: white;
            text-align: center;
        }
        
        .rsvp-form {
            max-width: 600px;
            margin: 0 auto;
            text-align: left;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: 500;
            color: #333;
        }
        
        .form-group input,
        .form-group textarea {
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 1rem;
            font-family: inherit;
        }
        
        .form-group textarea {
            resize: vertical;
            min-height: 100px;
        }
        
        .btn-submit {
            background: #333;
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 5px;
            font-size: 1.1rem;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        
        .btn-submit:hover {
            background: #555;
        }
        
        /* Footer */
        .footer {
            background: #333;
            color: white;
            text-align: center;
            padding: 40px 0;
        }
        
        .footer p {
            margin-bottom: 10px;
        }
        
        .social-links {
            margin-top: 20px;
        }
        
        .social-links a {
            color: white;
            font-size: 1.5rem;
            margin: 0 10px;
            text-decoration: none;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .cover-content h3 {
                font-size: 2rem;
            }
            
            .cover-content h1 {
                font-size: 3rem;
            }
            
            .couple-grid,
            .event-grid {
                grid-template-columns: 1fr;
                gap: 40px;
            }
            
            .gallery-grid {
                grid-template-columns: 1fr;
            }
            
            .section-title {
                font-size: 2.5rem;
            }
        }
        
        /* Hidden by default for animation */
        .hidden-content {
            display: none;
        }
    </style>
</head>
<body>
    <!-- Cover Section -->
    <section class="cover-section" id="cover">
        <div class="cover-content" data-aos="fade-up">
            <h3>{{ content.get('couple_names', 'Jimmy & Sherly') }}</h3>
            <h1>{{ content.get('hero_title', 'THE WEDDING OF') }}</h1>
            <div class="date">{{ content.get('wedding_date', 'SATURDAY, 21 AUGUST 2023') }}</div>
            <a href="#couple" class="btn-open">{{ content.get('open_button', 'Open Invitation') }}</a>
        </div>
    </section>

    <!-- Couple Section -->
    <section class="couple-section hidden-content" id="couple">
        <div class="container">
            <h2 class="section-title">{{ content.get('couple_section_title', 'The Couple') }}</h2>
            <div class="couple-grid">
                <div class="couple-member" data-aos="fade-right">
                    <h3>{{ content.get('groom_name', 'Jimmy') }}</h3>
                    <div class="role">{{ content.get('groom_role', 'The Groom') }}</div>
                    <p>{{ content.get('groom_bio', 'A kind-hearted man with a passion for music and adventure. He believes in the power of love and is excited to start this new chapter of life with his beloved Sherly.') }}</p>
                    <div class="parent-names">{{ content.get('groom_parents', 'Son of Mr. & Mrs. Anderson') }}</div>
                </div>
                <div class="couple-member" data-aos="fade-left">
                    <h3>{{ content.get('bride_name', 'Sherly') }}</h3>
                    <div class="role">{{ content.get('bride_role', 'The Bride') }}</div>
                    <p>{{ content.get('bride_bio', 'A beautiful soul with a love for art and nature. She dreams of a lifetime filled with love, laughter, and endless adventures with her best friend Jimmy.') }}</p>
                    <div class="parent-names">{{ content.get('bride_parents', 'Daughter of Mr. & Mrs. Williams') }}</div>
                </div>
            </div>
        </div>
    </section>

    <!-- Event Details Section -->
    <section class="event-section hidden-content" id="events">
        <div class="container">
            <h2 class="section-title">{{ content.get('event_section_title', 'Wedding Events') }}</h2>
            <div class="event-grid">
                <div class="event-card" data-aos="fade-up">
                    <h3>{{ content.get('ceremony_title', 'Wedding Ceremony') }}</h3>
                    <div class="date">{{ content.get('ceremony_date', 'Saturday, August 21, 2023') }}</div>
                    <div class="time">{{ content.get('ceremony_time', '10:00 AM - 12:00 PM') }}</div>
                    <div class="location">{{ content.get('ceremony_location', 'St. Mary\'s Catholic Church<br>123 Wedding Avenue<br>Downtown District')|safe }}</div>
                </div>
                <div class="event-card" data-aos="fade-up" data-aos-delay="200">
                    <h3>{{ content.get('reception_title', 'Wedding Reception') }}</h3>
                    <div class="date">{{ content.get('reception_date', 'Saturday, August 21, 2023') }}</div>
                    <div class="time">{{ content.get('reception_time', '6:00 PM - 10:00 PM') }}</div>
                    <div class="location">{{ content.get('reception_location', 'Grand Ballroom Hotel<br>456 Celebration Street<br>City Center')|safe }}</div>
                </div>
            </div>
        </div>
    </section>

    <!-- Gallery Section -->
    <section class="gallery-section hidden-content" id="gallery">
        <div class="container">
            <h2 class="section-title">{{ content.get('gallery_section_title', 'Our Gallery') }}</h2>
            <div class="gallery-grid">
                <div class="gallery-item" data-aos="fade-up">
                    <img src="{{ content.get('gallery_image_1', '/wp-content/uploads/2024/07/Foto-SLide-Gallery-1-Large-SHERLY-1-1.jpeg') }}" alt="Wedding Photo 1">
                </div>
                <div class="gallery-item" data-aos="fade-up" data-aos-delay="100">
                    <img src="{{ content.get('gallery_image_2', '/wp-content/uploads/2024/07/Foto-Slide-Gallery-15-Large-SHERLY.jpeg') }}" alt="Wedding Photo 2">
                </div>
                <div class="gallery-item" data-aos="fade-up" data-aos-delay="200">
                    <img src="{{ content.get('gallery_image_3', '/wp-content/uploads/2024/07/Fotno-Slide-Hitungan-Hari-2-Large-SHERLY-1.jpeg') }}" alt="Wedding Photo 3">
                </div>
            </div>
        </div>
    </section>

    <!-- RSVP Section -->
    <section class="rsvp-section hidden-content" id="rsvp">
        <div class="container">
            <h2 class="section-title">{{ content.get('rsvp_section_title', 'RSVP') }}</h2>
            <p style="font-size: 1.2rem; margin-bottom: 40px; color: #666;">{{ content.get('rsvp_description', 'We would love to celebrate with you! Please let us know if you can join us on our special day.') }}</p>
            <form class="rsvp-form">
                <div class="form-group">
                    <label>{{ content.get('form_name_label', 'Your Name') }}</label>
                    <input type="text" name="name" required>
                </div>
                <div class="form-group">
                    <label>{{ content.get('form_email_label', 'Email Address') }}</label>
                    <input type="email" name="email" required>
                </div>
                <div class="form-group">
                    <label>{{ content.get('form_guests_label', 'Number of Guests') }}</label>
                    <input type="number" name="guests" min="1" max="10" required>
                </div>
                <div class="form-group">
                    <label>{{ content.get('form_message_label', 'Message (Optional)') }}</label>
                    <textarea name="message"></textarea>
                </div>
                <button type="submit" class="btn-submit">{{ content.get('form_submit_button', 'Send RSVP') }}</button>
            </form>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer hidden-content">
        <div class="container">
            <p>{{ content.get('footer_text', 'With love and gratitude,') }}</p>
            <p style="font-family: 'Playfair Display', serif; font-size: 1.5rem;">{{ content.get('footer_couple', 'Jimmy & Sherly') }}</p>
            <div class="social-links">
                <a href="{{ content.get('instagram_link', '#') }}" target="_blank">📷 Instagram</a>
                <a href="{{ content.get('facebook_link', '#') }}" target="_blank">📘 Facebook</a>
            </div>
        </div>
    </footer>

    <script>
        // Initialize AOS
        AOS.init({
            duration: 1000,
            once: true
        });

        // Smooth scrolling and reveal content
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    // Reveal hidden content
                    document.querySelectorAll('.hidden-content').forEach(section => {
                        section.style.display = 'block';
                    });
                    
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // RSVP Form Handler
        document.querySelector('.rsvp-form').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const data = Object.fromEntries(formData);
            
            // Here you would typically send the data to your server
            alert('Thank you for your RSVP! We look forward to celebrating with you.');
            this.reset();
        });

        // Gallery Lightbox (simplified)
        document.querySelectorAll('.gallery-item img').forEach(img => {
            img.addEventListener('click', function() {
                const lightbox = document.createElement('div');
                lightbox.style.cssText = `
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0,0,0,0.9);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 1000;
                    cursor: pointer;
                `;
                
                const imgClone = this.cloneNode();
                imgClone.style.cssText = `
                    max-width: 90%;
                    max-height: 90%;
                    object-fit: contain;
                `;
                
                lightbox.appendChild(imgClone);
                document.body.appendChild(lightbox);
                
                lightbox.addEventListener('click', function() {
                    document.body.removeChild(lightbox);
                });
            });
        });
    </script>
</body>
</html>'''
    
    return render_template_string(html_template, content=content)

if __name__ == '__main__':
    print("Starting kaito2 dynamic server...")
    print("Running on http://localhost:5003")
    app.run(debug=True, port=5003, host='0.0.0.0')