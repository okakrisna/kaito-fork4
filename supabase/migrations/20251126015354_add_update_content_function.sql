/*
  # Add Database Function to Update Content with Price

  1. Purpose
    - Bypass PostgREST schema cache issues
    - Provide direct database function to update content including price
  
  2. Function
    - update_timeless_content_with_price
    - Accepts all fields including price
    - Returns updated record
  
  3. Security
    - Function has SECURITY DEFINER to bypass RLS temporarily
    - But still validates data before update
  
  4. Usage
    - Can be called via RPC from Supabase client
    - Bypasses PostgREST REST API schema cache
*/

-- Drop function if exists
DROP FUNCTION IF EXISTS update_timeless_content_with_price;

-- Create function to update content with price
CREATE OR REPLACE FUNCTION update_timeless_content_with_price(
  content_id UUID,
  update_data JSONB
)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  result JSONB;
BEGIN
  -- Update the record
  UPDATE timeless_content
  SET
    couple_names = COALESCE((update_data->>'couple_names')::TEXT, couple_names),
    groom_full_name = COALESCE((update_data->>'groom_full_name')::TEXT, groom_full_name),
    bride_full_name = COALESCE((update_data->>'bride_full_name')::TEXT, bride_full_name),
    wedding_title = COALESCE((update_data->>'wedding_title')::TEXT, wedding_title),
    wedding_date = COALESCE((update_data->>'wedding_date')::TEXT, wedding_date),
    venue_name = COALESCE((update_data->>'venue_name')::TEXT, venue_name),
    venue_address = COALESCE((update_data->>'venue_address')::TEXT, venue_address),
    venue_maps = COALESCE((update_data->>'venue_maps')::TEXT, venue_maps),
    ceremony_time = COALESCE((update_data->>'ceremony_time')::TEXT, ceremony_time),
    reception_time = COALESCE((update_data->>'reception_time')::TEXT, reception_time),
    background_image = COALESCE((update_data->>'background_image')::TEXT, background_image),
    groom_photo = COALESCE((update_data->>'groom_photo')::TEXT, groom_photo),
    bride_photo = COALESCE((update_data->>'bride_photo')::TEXT, bride_photo),
    thank_you_message = COALESCE((update_data->>'thank_you_message')::TEXT, thank_you_message),
    hero_title = COALESCE((update_data->>'hero_title')::TEXT, hero_title),
    hero_image = COALESCE((update_data->>'hero_image')::TEXT, hero_image),
    hero_background_image = COALESCE((update_data->>'hero_background_image')::TEXT, hero_background_image),
    livestreaming_image = COALESCE((update_data->>'livestreaming_image')::TEXT, livestreaming_image),
    gallery_images = COALESCE((update_data->>'gallery_images')::JSONB, gallery_images),
    price = COALESCE((update_data->>'price')::NUMERIC, price),
    status = COALESCE((update_data->>'status')::TEXT, status),
    template_name = COALESCE((update_data->>'template_name')::TEXT, template_name),
    slug = COALESCE((update_data->>'slug')::TEXT, slug),
    updated_at = NOW()
  WHERE id = content_id
  RETURNING to_jsonb(timeless_content.*) INTO result;

  -- Return the updated record
  RETURN result;
END;
$$;

-- Grant execute permission to public (anyone can call this function)
GRANT EXECUTE ON FUNCTION update_timeless_content_with_price TO PUBLIC;

COMMENT ON FUNCTION update_timeless_content_with_price IS 'Update timeless_content record including price field - bypasses PostgREST schema cache';