import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "npm:@supabase/supabase-js@2.39.3";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Client-Info, Apikey",
};

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") {
    return new Response(null, {
      status: 200,
      headers: corsHeaders,
    });
  }

  try {
    const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
    const supabaseServiceKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;

    const supabase = createClient(supabaseUrl, supabaseServiceKey, {
      auth: {
        persistSession: false,
      },
    });

    const requestData = await req.json();
    console.log("Received data:", requestData);

    const {
      id,
      couple_names,
      groom_full_name,
      bride_full_name,
      wedding_title,
      wedding_date,
      venue_name,
      venue_address,
      venue_maps,
      ceremony_time,
      reception_time,
      background_image,
      groom_photo,
      bride_photo,
      thank_you_message,
      hero_title,
      hero_image,
      hero_background_image,
      livestreaming_image,
      background_section_1,
      background_section_1_size,
      background_section_1_position,
      background_section_2,
      background_section_2_size,
      background_section_2_position,
      background_section_3,
      background_section_3_size,
      background_section_3_position,
      background_section_4,
      background_section_4_size,
      background_section_4_position,
      background_section_5,
      background_section_5_size,
      background_section_5_position,
      gallery_images,
      price,
      template_name,
      slug,
      status,
      password_protected,
      invitation_password,
      is_published,
    } = requestData;

    let result;

    if (id) {
      // Update existing record
      console.log("Updating record with ID:", id);

      const { data, error } = await supabase
        .from("timeless_content")
        .update({
          couple_names,
          groom_full_name,
          bride_full_name,
          wedding_title,
          wedding_date,
          venue_name,
          venue_address,
          venue_maps,
          ceremony_time,
          reception_time,
          background_image,
          groom_photo,
          bride_photo,
          thank_you_message,
          hero_title,
          hero_image,
          hero_background_image,
          livestreaming_image,
          background_section_1,
          background_section_1_size,
          background_section_1_position,
          background_section_2,
          background_section_2_size,
          background_section_2_position,
          background_section_3,
          background_section_3_size,
          background_section_3_position,
          background_section_4,
          background_section_4_size,
          background_section_4_position,
          background_section_5,
          background_section_5_size,
          background_section_5_position,
          gallery_images,
          price,
          template_name,
          slug,
          status,
          password_protected,
          invitation_password,
          is_published,
          updated_at: new Date().toISOString(),
        })
        .eq("id", id)
        .select()
        .single();

      if (error) {
        console.error("Update error:", error);
        throw error;
      }

      result = data;
    } else {
      // Insert new record
      console.log("Inserting new record");

      const { data, error } = await supabase
        .from("timeless_content")
        .insert({
          couple_names,
          groom_full_name,
          bride_full_name,
          wedding_title,
          wedding_date,
          venue_name,
          venue_address,
          venue_maps,
          ceremony_time,
          reception_time,
          background_image,
          groom_photo,
          bride_photo,
          thank_you_message,
          hero_title,
          hero_image,
          hero_background_image,
          livestreaming_image,
          background_section_1,
          background_section_1_size,
          background_section_1_position,
          background_section_2,
          background_section_2_size,
          background_section_2_position,
          background_section_3,
          background_section_3_size,
          background_section_3_position,
          background_section_4,
          background_section_4_size,
          background_section_4_position,
          background_section_5,
          background_section_5_size,
          background_section_5_position,
          gallery_images,
          price,
          template_name,
          slug,
          status,
          password_protected,
          invitation_password,
          is_published,
        })
        .select()
        .single();

      if (error) {
        console.error("Insert error:", error);
        throw error;
      }

      result = data;
    }

    console.log("Save successful:", result);

    return new Response(JSON.stringify({ success: true, data: result }), {
      headers: {
        ...corsHeaders,
        "Content-Type": "application/json",
      },
    });
  } catch (error) {
    console.error("Error:", error);

    return new Response(
      JSON.stringify({
        success: false,
        error: error.message || "Unknown error occurred",
      }),
      {
        status: 400,
        headers: {
          ...corsHeaders,
          "Content-Type": "application/json",
        },
      }
    );
  }
});
