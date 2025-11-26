/*
  # Create raw SQL update function to bypass PostgREST schema cache

  1. Functions
    - `raw_update_timeless_content` - Direct SQL UPDATE bypassing PostgREST
    - `raw_insert_timeless_content` - Direct SQL INSERT bypassing PostgREST
  
  2. Security
    - Functions are SECURITY DEFINER (run as creator)
    - Allow public access for development
*/

-- Function to update timeless_content using raw SQL (bypasses PostgREST cache)
CREATE OR REPLACE FUNCTION raw_update_timeless_content(
  record_id uuid,
  data jsonb
)
RETURNS jsonb
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  result jsonb;
BEGIN
  -- Build and execute dynamic UPDATE query
  EXECUTE format(
    'UPDATE timeless_content SET 
      couple_names = COALESCE(($1->>%L)::text, couple_names),
      groom_full_name = COALESCE(($1->>%L)::text, groom_full_name),
      bride_full_name = COALESCE(($1->>%L)::text, bride_full_name),
      wedding_title = COALESCE(($1->>%L)::text, wedding_title),
      wedding_date = COALESCE(($1->>%L)::timestamptz, wedding_date),
      venue_name = COALESCE(($1->>%L)::text, venue_name),
      venue_address = COALESCE(($1->>%L)::text, venue_address),
      venue_maps = COALESCE(($1->>%L)::text, venue_maps),
      ceremony_time = COALESCE(($1->>%L)::text, ceremony_time),
      reception_time = COALESCE(($1->>%L)::text, reception_time),
      background_image = COALESCE(($1->>%L)::text, background_image),
      groom_photo = COALESCE(($1->>%L)::text, groom_photo),
      bride_photo = COALESCE(($1->>%L)::text, bride_photo),
      thank_you_message = COALESCE(($1->>%L)::text, thank_you_message),
      hero_title = COALESCE(($1->>%L)::text, hero_title),
      hero_image = COALESCE(($1->>%L)::text, hero_image),
      hero_background_image = COALESCE(($1->>%L)::text, hero_background_image),
      livestreaming_image = COALESCE(($1->>%L)::text, livestreaming_image),
      background_section_1 = COALESCE(($1->>%L)::text, background_section_1),
      background_section_1_size = COALESCE(($1->>%L)::text, background_section_1_size),
      background_section_1_position = COALESCE(($1->>%L)::text, background_section_1_position),
      background_section_2 = COALESCE(($1->>%L)::text, background_section_2),
      background_section_2_size = COALESCE(($1->>%L)::text, background_section_2_size),
      background_section_2_position = COALESCE(($1->>%L)::text, background_section_2_position),
      background_section_3 = COALESCE(($1->>%L)::text, background_section_3),
      background_section_3_size = COALESCE(($1->>%L)::text, background_section_3_size),
      background_section_3_position = COALESCE(($1->>%L)::text, background_section_3_position),
      background_section_4 = COALESCE(($1->>%L)::text, background_section_4),
      background_section_4_size = COALESCE(($1->>%L)::text, background_section_4_size),
      background_section_4_position = COALESCE(($1->>%L)::text, background_section_4_position),
      background_section_5 = COALESCE(($1->>%L)::text, background_section_5),
      background_section_5_size = COALESCE(($1->>%L)::text, background_section_5_size),
      background_section_5_position = COALESCE(($1->>%L)::text, background_section_5_position),
      gallery_images = COALESCE(($1->%L)::jsonb, gallery_images),
      price = COALESCE(($1->>%L)::integer, price),
      template_name = COALESCE(($1->>%L)::text, template_name),
      slug = COALESCE(($1->>%L)::text, slug),
      status = COALESCE(($1->>%L)::text, status),
      password_protected = COALESCE(($1->>%L)::boolean, password_protected),
      invitation_password = COALESCE(($1->>%L)::text, invitation_password),
      is_published = COALESCE(($1->>%L)::boolean, is_published),
      updated_at = NOW()
    WHERE id = $2
    RETURNING row_to_json(timeless_content.*)',
    'couple_names', 'groom_full_name', 'bride_full_name', 'wedding_title', 'wedding_date',
    'venue_name', 'venue_address', 'venue_maps', 'ceremony_time', 'reception_time',
    'background_image', 'groom_photo', 'bride_photo', 'thank_you_message', 'hero_title',
    'hero_image', 'hero_background_image', 'livestreaming_image',
    'background_section_1', 'background_section_1_size', 'background_section_1_position',
    'background_section_2', 'background_section_2_size', 'background_section_2_position',
    'background_section_3', 'background_section_3_size', 'background_section_3_position',
    'background_section_4', 'background_section_4_size', 'background_section_4_position',
    'background_section_5', 'background_section_5_size', 'background_section_5_position',
    'gallery_images', 'price', 'template_name', 'slug', 'status',
    'password_protected', 'invitation_password', 'is_published'
  )
  INTO result
  USING data, record_id;
  
  RETURN result;
END;
$$;

-- Function to insert timeless_content using raw SQL (bypasses PostgREST cache)
CREATE OR REPLACE FUNCTION raw_insert_timeless_content(data jsonb)
RETURNS jsonb
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  result jsonb;
BEGIN
  INSERT INTO timeless_content (
    couple_names, groom_full_name, bride_full_name, wedding_title, wedding_date,
    venue_name, venue_address, venue_maps, ceremony_time, reception_time,
    background_image, groom_photo, bride_photo, thank_you_message, hero_title,
    hero_image, hero_background_image, livestreaming_image,
    background_section_1, background_section_1_size, background_section_1_position,
    background_section_2, background_section_2_size, background_section_2_position,
    background_section_3, background_section_3_size, background_section_3_position,
    background_section_4, background_section_4_size, background_section_4_position,
    background_section_5, background_section_5_size, background_section_5_position,
    gallery_images, price, template_name, slug, status,
    password_protected, invitation_password, is_published
  )
  VALUES (
    data->>'couple_names', data->>'groom_full_name', data->>'bride_full_name',
    data->>'wedding_title', (data->>'wedding_date')::timestamptz,
    data->>'venue_name', data->>'venue_address', data->>'venue_maps',
    data->>'ceremony_time', data->>'reception_time',
    data->>'background_image', data->>'groom_photo', data->>'bride_photo',
    data->>'thank_you_message', data->>'hero_title',
    data->>'hero_image', data->>'hero_background_image', data->>'livestreaming_image',
    data->>'background_section_1', data->>'background_section_1_size', data->>'background_section_1_position',
    data->>'background_section_2', data->>'background_section_2_size', data->>'background_section_2_position',
    data->>'background_section_3', data->>'background_section_3_size', data->>'background_section_3_position',
    data->>'background_section_4', data->>'background_section_4_size', data->>'background_section_4_position',
    data->>'background_section_5', data->>'background_section_5_size', data->>'background_section_5_position',
    (data->'gallery_images')::jsonb, (data->>'price')::integer,
    data->>'template_name', data->>'slug', data->>'status',
    (data->>'password_protected')::boolean, data->>'invitation_password', (data->>'is_published')::boolean
  )
  RETURNING row_to_json(timeless_content.*)
  INTO result;
  
  RETURN result;
END;
$$;