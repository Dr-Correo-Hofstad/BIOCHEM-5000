// ====================================================================
// DESIGN STANDARDS: RT Helical Structural Engineering Block
// Data-Driven Automation: Highlighting and Filtering Null Nodes
// ====================================================================

$fn = 40;

// Golden Ratio Constants
golden_angle = 137.5077;
node_count = 150;
scaling_factor = 4.5;
vertical_pitch = 0.4;

// Operational control flag: 1 = Highlight Nulls, 0 = Omit/Filter Nulls entirely
render_mode = 1; 

// Ingest the external JSON array compiled by the verification tool
null_data = read_json("null_nodes.json");
null_array = null_data.null_node_ids;

function is_null_node(id, list, index=0) = 
    index >= len(list) ? false : 
    list[index] == id ? true : 
    is_null_node(id, list, index + 1);

module generate_adaptive_spiral() {
    echo("[*] Executing structural data-driven rendering pass...");
    
    for (i = [1 : node_count]) {
        angle = i * golden_angle;
        radius = scaling_factor * sqrt(i);
        
        pos_x = radius * cos(angle);
        pos_y = radius * sin(angle);
        pos_z = i * vertical_pitch;
        
        is_null = is_null_node(i, null_array);
        
        if (is_null) {
            if (render_mode == 1) {
                // Highlight Mode: Color destructive interference nodes deep Crimson
                translate([pos_x, pos_y, pos_z])
                    color("Crimson", 1.0)
                        sphere(r = 2.5); // Enlarged for tracking visualization
            }
            // If render_mode == 0, the node loop bypasses geometry rendering entirely
        } else {
            // Standard Active Node Path Rendering
            translate([pos_x, pos_y, pos_z])
                color("Teal", 0.6)
                    sphere(r = 1.8);
        }
    }
}

// System Compilation Rendering
union() {
    generate_adaptive_spiral();
    color("Gold", 0.3)
        cylinder(h = node_count * vertical_pitch + 5, r = 2.0, center = false);
}
