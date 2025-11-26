/*
  # Add Missing Fields to Timeless Content Table

  1. Changes
    - Add `price` column (numeric) for template pricing
    - Add `template_name` column (text) for template identification
    - Add `slug` column (text) for URL-friendly identifier
    - Add `status` column (text) for workflow status tracking
    - Add `password_protected` column (boolean) for privacy settings
    - Add `invitation_password` column (text) for password protection
    - Add `is_published` column (boolean) for publish status
  
  2. Purpose
    - Complete the table structure for full wedding invitation management
    - Enable pricing, templates, security, and workflow features
*/

-- Add price column
ALTER TABLE timeless_content 
ADD COLUMN IF NOT EXISTS price numeric(10, 2) DEFAULT 0;

-- Add template_name column
ALTER TABLE timeless_content 
ADD COLUMN IF NOT EXISTS template_name text DEFAULT 'timeless';

-- Add slug column
ALTER TABLE timeless_content 
ADD COLUMN IF NOT EXISTS slug text DEFAULT '';

-- Add status column
ALTER TABLE timeless_content 
ADD COLUMN IF NOT EXISTS status text DEFAULT 'draft';

-- Add password_protected column
ALTER TABLE timeless_content 
ADD COLUMN IF NOT EXISTS password_protected boolean DEFAULT false;

-- Add invitation_password column
ALTER TABLE timeless_content 
ADD COLUMN IF NOT EXISTS invitation_password text DEFAULT '';

-- Add is_published column
ALTER TABLE timeless_content 
ADD COLUMN IF NOT EXISTS is_published boolean DEFAULT false;

-- Create index on slug for faster lookups
CREATE INDEX IF NOT EXISTS idx_timeless_content_slug ON timeless_content(slug);

-- Create index on template_name for filtering
CREATE INDEX IF NOT EXISTS idx_timeless_content_template_name ON timeless_content(template_name);
