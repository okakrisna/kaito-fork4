/*
  # Add Status and Workflow Fields

  1. Changes
    - Add `status` column with values: 'in_progress', 'completed'
    - Add `template_name` column for template type
    - Add `slug` column for URL slug
    - Add `completed_at` timestamp for tracking completion
    - Set default status to 'in_progress' for all existing records
    
  2. Notes
    - All existing templates will be set to 'in_progress' status
    - This enables the Dashboard → Orders workflow
*/

-- Add status column with default 'in_progress'
ALTER TABLE timeless_content 
ADD COLUMN IF NOT EXISTS status text DEFAULT 'in_progress';

-- Add template_name column
ALTER TABLE timeless_content 
ADD COLUMN IF NOT EXISTS template_name text DEFAULT 'timeless';

-- Add slug column
ALTER TABLE timeless_content 
ADD COLUMN IF NOT EXISTS slug text;

-- Add completed_at timestamp
ALTER TABLE timeless_content 
ADD COLUMN IF NOT EXISTS completed_at timestamptz;

-- Update existing records to have 'in_progress' status
UPDATE timeless_content 
SET status = 'in_progress' 
WHERE status IS NULL;

-- Create index for status queries
CREATE INDEX IF NOT EXISTS idx_timeless_content_status ON timeless_content(status);

-- Create index for slug lookups
CREATE INDEX IF NOT EXISTS idx_timeless_content_slug ON timeless_content(slug);
