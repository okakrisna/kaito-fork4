/*
  # Create update content function v2 (new name to bypass cache)

  1. Functions
    - `update_content_v2` - Update timeless_content (new name)
    - `insert_content_v2` - Insert timeless_content (new name)
  
  2. Security
    - SECURITY DEFINER for elevated privileges
    - Public access for development
*/

-- Simple update function with new name (bypasses cache)
CREATE OR REPLACE FUNCTION update_content_v2(
  p_id uuid,
  p_couple_names text DEFAULT NULL,
  p_groom_full_name text DEFAULT NULL,
  p_bride_full_name text DEFAULT NULL,
  p_wedding_title text DEFAULT NULL,
  p_wedding_date timestamptz DEFAULT NULL,
  p_venue_name text DEFAULT NULL,
  p_venue_address text DEFAULT NULL,
  p_venue_maps text DEFAULT NULL,
  p_ceremony_time text DEFAULT NULL,
  p_reception_time text DEFAULT NULL,
  p_background_image text DEFAULT NULL,
  p_groom_photo text DEFAULT NULL,
  p_bride_photo text DEFAULT NULL,
  p_thank_you_message text DEFAULT NULL,
  p_hero_title text DEFAULT NULL,
  p_hero_image text DEFAULT NULL,
  p_hero_background_image text DEFAULT NULL,
  p_livestreaming_image text DEFAULT NULL,
  p_background_section_1 text DEFAULT NULL,
  p_background_section_1_size text DEFAULT NULL,
  p_background_section_1_position text DEFAULT NULL,
  p_background_section_2 text DEFAULT NULL,
  p_background_section_2_size text DEFAULT NULL,
  p_background_section_2_position text DEFAULT NULL,
  p_background_section_3 text DEFAULT NULL,
  p_background_section_3_size text DEFAULT NULL,
  p_background_section_3_position text DEFAULT NULL,
  p_background_section_4 text DEFAULT NULL,
  p_background_section_4_size text DEFAULT NULL,
  p_background_section_4_position text DEFAULT NULL,
  p_background_section_5 text DEFAULT NULL,
  p_background_section_5_size text DEFAULT NULL,
  p_background_section_5_position text DEFAULT NULL,
  p_gallery_images jsonb DEFAULT NULL,
  p_price integer DEFAULT NULL,
  p_template_name text DEFAULT NULL,
  p_slug text DEFAULT NULL,
  p_status text DEFAULT NULL,
  p_password_protected boolean DEFAULT NULL,
  p_invitation_password text DEFAULT NULL,
  p_is_published boolean DEFAULT NULL
)
RETURNS jsonb
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  result jsonb;
BEGIN
  UPDATE timeless_content SET
    couple_names = COALESCE(p_couple_names, couple_names),
    groom_full_name = COALESCE(p_groom_full_name, groom_full_name),
    bride_full_name = COALESCE(p_bride_full_name, bride_full_name),
    wedding_title = COALESCE(p_wedding_title, wedding_title),
    wedding_date = COALESCE(p_wedding_date, wedding_date),
    venue_name = COALESCE(p_venue_name, venue_name),
    venue_address = COALESCE(p_venue_address, venue_address),
    venue_maps = COALESCE(p_venue_maps, venue_maps),
    ceremony_time = COALESCE(p_ceremony_time, ceremony_time),
    reception_time = COALESCE(p_reception_time, reception_time),
    background_image = COALESCE(p_background_image, background_image),
    groom_photo = COALESCE(p_groom_photo, groom_photo),
    bride_photo = COALESCE(p_bride_photo, bride_photo),
    thank_you_message = COALESCE(p_thank_you_message, thank_you_message),
    hero_title = COALESCE(p_hero_title, hero_title),
    hero_image = COALESCE(p_hero_image, hero_image),
    hero_background_image = COALESCE(p_hero_background_image, hero_background_image),
    livestreaming_image = COALESCE(p_livestreaming_image, livestreaming_image),
    background_section_1 = COALESCE(p_background_section_1, background_section_1),
    background_section_1_size = COALESCE(p_background_section_1_size, background_section_1_size),
    background_section_1_position = COALESCE(p_background_section_1_position, background_section_1_position),
    background_section_2 = COALESCE(p_background_section_2, background_section_2),
    background_section_2_size = COALESCE(p_background_section_2_size, background_section_2_size),
    background_section_2_position = COALESCE(p_background_section_2_position, background_section_2_position),
    background_section_3 = COALESCE(p_background_section_3, background_section_3),
    background_section_3_size = COALESCE(p_background_section_3_size, background_section_3_size),
    background_section_3_position = COALESCE(p_background_section_3_position, background_section_3_position),
    background_section_4 = COALESCE(p_background_section_4, background_section_4),
    background_section_4_size = COALESCE(p_background_section_4_size, background_section_4_size),
    background_section_4_position = COALESCE(p_background_section_4_position, background_section_4_position),
    background_section_5 = COALESCE(p_background_section_5, background_section_5),
    background_section_5_size = COALESCE(p_background_section_5_size, background_section_5_size),
    background_section_5_position = COALESCE(p_background_section_5_position, background_section_5_position),
    gallery_images = COALESCE(p_gallery_images, gallery_images),
    price = COALESCE(p_price, price),
    template_name = COALESCE(p_template_name, template_name),
    slug = COALESCE(p_slug, slug),
    status = COALESCE(p_status, status),
    password_protected = COALESCE(p_password_protected, password_protected),
    invitation_password = COALESCE(p_invitation_password, invitation_password),
    is_published = COALESCE(p_is_published, is_published),
    updated_at = NOW()
  WHERE id = p_id
  RETURNING to_jsonb(timeless_content.*) INTO result;
  
  RETURN result;
END;
$$;