// ====================================================================
// DESIGN STANDARDS: RT Mechanical Integration Assembly Block
// Component: Olfactory Manifold-to-Chassis Alignment Bracket
// ====================================================================

$fn = 60; // Production grade curves for structural fastner paths

// Import dimensional metrics from your standard manifold design parameters
manifold_x_dim = 95.0;
manifold_y_dim = 65.0;
manifold_z_dim = 40.0;
intake_radius  = 4.5;

// Mainframe Chassis Grid Specifications (Standardized server rail matrix)
grid_pitch_x = 25.0;
grid_pitch_y = 20.0;
bracket_thick = 4.0;

module chassis_mounting_grid_plate() {
    // Generates the interface adapter plate that locks to the chassis rails
    difference() {
        // Base plate surface padding out the manifold footprint bounds
        color("SlateGray", 0.5)
            cube([manifold_x_dim + 30, manifold_y_dim + 20, bracket_thick], center = true);
            
        // 1. Core Airflow Access Aperture (Pass-through clearance for sinuous intake paths)
        cube([manifold_x_dim - 10, manifold_y_dim - 10, bracket_thick + 2], center = true);
        
        // 2. Standardized Server Chassis Anchor Holes (Outer perimeter array)
        for (x = [-2 : 2]) {
            for (y = [-1 : 1]) {
                if (abs(x) == 2 || abs(y) == 1) {
                    translate([x * grid_pitch_x, y * grid_pitch_y, 0])
                        cylinder(h = bracket_thick + 2, r = 2.2, center = true); // M4 screw clearance
                }
            }
        }
    }
}

module manifold_alignment_clips() {
    // Vertical alignment guide rails that clamp the manifold block securely on the X/Y axes
    color("DarkPolymer", 1.0) {
        // Left Guide Rail
        translate([-(manifold_x_dim / 2 + bracket_thick / 2), 0, (manifold_z_dim / 4)])
            cube([bracket_thick, manifold_y_dim, manifold_z_dim / 2], center = true);
            
        // Right Guide Rail
        translate([(manifold_x_dim / 2 + bracket_thick / 2), 0, (manifold_z_dim / 4)])
            cube([bracket_thick, manifold_y_dim, manifold_z_dim / 2], center = true);
    }
}

// ====================================================================
// SYSTEM COMPILATION: TOP-LEVEL MECHANICAL ASSEMBLY
// ====================================================================

// 1. Instantiate the rigid structural base grounding alignment assembly
translate([0, 0, -(bracket_thick / 2)]) {
    chassis_mounting_grid_plate();
    manifold_alignment_clips();
}

// 2. Reference Assembly Layer: Simulates the olfactory_intake_manifold seating position
// In production, this can be replaced by an external include statement
translate([0, 0, (manifold_z_dim / 2)]) {
    difference() {
        // Manifold Body Representation
        color("MediumPurple", 0.3)
            cube([manifold_x_dim, manifold_y_dim, manifold_z_dim], center = true);
            
        // Sinuous Airflow Passages (Visualization only)
        for (offset_y = [-16, 0, 16]) {
            translate([0, offset_y, 4])
                rotate([0, 90, 0])
                    cylinder(h = manifold_x_dim + 5, r = intake_radius, center = true);
        }
    }
}
