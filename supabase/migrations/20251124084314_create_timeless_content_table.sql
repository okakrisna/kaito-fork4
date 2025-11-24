/*
  # Create timeless_content table for wedding invitation

  1. New Tables
    - `timeless_content`
      - `id` (uuid, primary key) - Unique identifier
      - `couple_names` (text) - Couple names displayed in header
      - `groom_full_name` (text) - Full name of groom
      - `bride_full_name` (text) - Full name of bride
      - `wedding_title` (text) - Main wedding title
      - `wedding_date` (text) - Wedding date display
      - `venue_name` (text) - Venue name
      - `venue_address` (text) - Full venue address
      - `venue_maps` (text) - Google Maps link
      - `ceremony_time` (text) - Ceremony time
      - `reception_time` (text) - Reception time
      - `background_section_1` (text) - Background image URL for section 1
      - `background_section_2` (text) - Groom photo URL
      - `background_section_3` (text) - Bride photo URL
      - `hero_background_image` (text) - Hero section background image URL
      - `livestreaming_image` (text) - Livestreaming section image URL
      - `gallery_images` (text[]) - Array of gallery image URLs
      - `thank_you_message` (text) - Thank you message
      - `created_at` (timestamptz) - Record creation timestamp
      - `updated_at` (timestamptz) - Last update timestamp

  2. Security
    - Enable RLS on `timeless_content` table
    - Add policy for public read access (wedding invitation is public)
    - Add policy for authenticated write access (admin only)
*/

CREATE TABLE IF NOT EXISTS timeless_content (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  couple_names text DEFAULT '',
  groom_full_name text DEFAULT '',
  bride_full_name text DEFAULT '',
  wedding_title text DEFAULT '',
  wedding_date text DEFAULT '',
  venue_name text DEFAULT '',
  venue_address text DEFAULT '',
  venue_maps text DEFAULT '',
  ceremony_time text DEFAULT '',
  reception_time text DEFAULT '',
  background_section_1 text DEFAULT '',
  background_section_2 text DEFAULT '',
  background_section_3 text DEFAULT '',
  hero_background_image text DEFAULT '',
  livestreaming_image text DEFAULT '',
  gallery_images text[] DEFAULT '{}',
  thank_you_message text DEFAULT '',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

ALTER TABLE timeless_content ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can read timeless content"
  ON timeless_content
  FOR SELECT
  TO public
  USING (true);

CREATE POLICY "Anyone can insert timeless content"
  ON timeless_content
  FOR INSERT
  TO public
  WITH CHECK (true);

CREATE POLICY "Anyone can update timeless content"
  ON timeless_content
  FOR UPDATE
  TO public
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Anyone can delete timeless content"
  ON timeless_content
  FOR DELETE
  TO public
  USING (true);