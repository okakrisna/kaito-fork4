import { createClient } from 'npm:@supabase/supabase-js@2';

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Client-Info, Apikey',
};

Deno.serve(async (req: Request) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, {
      status: 200,
      headers: corsHeaders,
    });
  }

  try {
    const { id, data } = await req.json();

    if (!id) {
      return new Response(
        JSON.stringify({ error: 'ID is required' }),
        {
          status: 400,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        }
      );
    }

    // Create Supabase admin client
    const supabaseUrl = Deno.env.get('SUPABASE_URL')!;
    const supabaseServiceKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
    const supabase = createClient(supabaseUrl, supabaseServiceKey);

    // Build UPDATE query dynamically
    const updateFields: string[] = [];
    const updateValues: any[] = [];
    let paramIndex = 1;

    const fieldMap: Record<string, string> = {
      couple_names: 'text',
      groom_full_name: 'text',
      bride_full_name: 'text',
      wedding_title: 'text',
      wedding_date: 'timestamptz',
      venue_name: 'text',
      venue_address: 'text',
      venue_maps: 'text',
      ceremony_time: 'text',
      reception_time: 'text',
      background_image: 'text',
      groom_photo: 'text',
      bride_photo: 'text',
      thank_you_message: 'text',
      hero_title: 'text',
      hero_image: 'text',
      hero_background_image: 'text',
      livestreaming_image: 'text',
      background_section_1: 'text',
      background_section_1_size: 'text',
      background_section_1_position: 'text',
      background_section_2: 'text',
      background_section_2_size: 'text',
      background_section_2_position: 'text',
      background_section_3: 'text',
      background_section_3_size: 'text',
      background_section_3_position: 'text',
      background_section_4: 'text',
      background_section_4_size: 'text',
      background_section_4_position: 'text',
      background_section_5: 'text',
      background_section_5_size: 'text',
      background_section_5_position: 'text',
      gallery_images: 'jsonb',
      price: 'integer',
      template_name: 'text',
      slug: 'text',
      status: 'text',
      password_protected: 'boolean',
      invitation_password: 'text',
      is_published: 'boolean',
    };

    for (const [key, type] of Object.entries(fieldMap)) {
      if (data[key] !== undefined && data[key] !== null) {
        if (type === 'jsonb') {
          updateFields.push(`${key} = $${paramIndex}::jsonb`);
          updateValues.push(JSON.stringify(data[key]));
        } else if (type === 'integer') {
          updateFields.push(`${key} = $${paramIndex}::integer`);
          updateValues.push(parseInt(data[key]));
        } else if (type === 'boolean') {
          updateFields.push(`${key} = $${paramIndex}::boolean`);
          updateValues.push(data[key]);
        } else if (type === 'timestamptz') {
          updateFields.push(`${key} = $${paramIndex}::timestamptz`);
          updateValues.push(data[key]);
        } else {
          updateFields.push(`${key} = $${paramIndex}`);
          updateValues.push(data[key]);
        }
        paramIndex++;
      }
    }

    if (updateFields.length === 0) {
      return new Response(
        JSON.stringify({ error: 'No fields to update' }),
        {
          status: 400,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        }
      );
    }

    // Add updated_at
    updateFields.push('updated_at = NOW()');

    // Execute raw SQL update
    const query = `
      UPDATE timeless_content 
      SET ${updateFields.join(', ')}
      WHERE id = $${paramIndex}::uuid
      RETURNING *
    `;

    updateValues.push(id);

    console.log('Executing query:', query);
    console.log('With values:', updateValues);

    const { data: result, error } = await supabase.rpc('exec_sql', {
      query: query,
      params: updateValues
    }).single();

    if (error) {
      console.error('Update error:', error);
      return new Response(
        JSON.stringify({ error: error.message }),
        {
          status: 500,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        }
      );
    }

    return new Response(
      JSON.stringify(result),
      {
        status: 200,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      }
    );
  } catch (error) {
    console.error('Function error:', error);
    return new Response(
      JSON.stringify({ error: error.message }),
      {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      }
    );
  }
});