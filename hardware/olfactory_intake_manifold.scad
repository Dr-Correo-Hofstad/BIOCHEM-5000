// ====================================================================
// DESIGN STANDARDS: RT Olfactory Detection Block
// Modeling Nasal Intake Manifolds and Electrostatic Receptor Grid Slots
// ====================================================================

$fn = 80; // Optimize boundary curves for complex gas-phase ingestion paths

// Parametric Dimensional Coordinates (All metrics in millimeters)
manifold_x_dim = 95.0;
manifold_y_dim = 65.0;
manifold_z_dim = 40.0;
intake_radius  = 4.5;
sensor_slot_w  = 22.0;
sensor_slot_d  = 2.0;

module nasal_intake_manifold() {
    difference() {
        // Primary Structural Housing Substrate
        color("MediumPurple", 0.6)
            cube([manifold_x_dim, manifold_y_dim, manifold_z_dim], center = true);
            
        // --- Sinuous Ingestion Channel Arrays ---
        // Simulates aerodynamic gas distribution paths across the tracking field
        for (offset_y = [-16, 0, 16]) {
            translate([0, offset_y, 4]) {
                rotate([0, 90, 0]) {
                    // Core airflow channels
                    cylinder(h = manifold_x_dim + 5, r = intake_radius, center = true);
                }
            }
        }
        
        // Vertical Venturi Vias (Inter-channel gas cross-flows)
        for (offset_x = [-25, 25]) {
            translate([offset_x, 0, 4])
                cylinder(h = 25.0, r = intake_radius * 0.7, center = true);
        }
        
        // --- Electrostatic Receptor Array Card Slots ---
        // Physical pocket cuts where the electronic sensor boards intersect airflow lines
        for (slot_x = [-20, 0, 20]) {
            translate([slot_x, 0, -6]) {
                cube([sensor_slot_d, manifold_y_dim - 10, manifold_z_dim / 2], center = true);
            }
        }
    }
}

module pneumatic_coupling_collars() {
    // Rigid physical attachment flanges for connecting external gas feed lines
    color("DimGray", 1.0) {
        for (offset_y = [-16, 0, 16]) {
            translate([-(manifold_x_dim / 2 + 2), offset_y, 4])
                rotate([0, 90, 0])
                    difference() {
                        cylinder(h = 5.0, r = intake_radius + 2.5, center = true);
                        cylinder(h = 6.0, r = intake_radius, center = true);
                    }
        }
    }
}

// Assemble Olfactory Sub-Chassis Block
union() {
    nasal_intake_manifold();
    pneumatic_coupling_collars();
}
