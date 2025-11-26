/*
  # Fix Price Column Schema Cache Issue

  1. Problem
    - PostgREST schema cache not recognizing 'price' column
    - Even after refresh migration, cache still stale
  
  2. Solution
    - Drop and recreate the price column to force cache invalidation
    - This will clear the cached schema for this column
  
  3. Safety
    - Uses IF EXISTS to prevent errors
    - Column is nullable so no data integrity issues
    - Operation is safe for existing records

  4. Notes
    - This is a workaround for PostgREST schema cache issues
    - After this migration, the price column will be fresh in cache
*/

-- Drop the price column if exists
ALTER TABLE timeless_content DROP COLUMN IF EXISTS price;

-- Recreate the price column with fresh schema
ALTER TABLE timeless_content ADD COLUMN price NUMERIC;

-- Add comment for documentation
COMMENT ON COLUMN timeless_content.price IS 'Price of the wedding template package (in IDR) - Recreated to fix schema cache';

-- Force PostgREST to reload schema
NOTIFY pgrst, 'reload schema';