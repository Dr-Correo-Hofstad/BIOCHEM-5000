// ====================================================================
// DESIGN STANDARDS: RT Vestibular Acoustic Transceiver Array
// Modeling Three-Axis Semicircular Intrabody Fluidic Accelerometers
// ====================================================================

$fn = 80;

// Structural Enclosure Metrics (Dimensions scaled in millimeters)
housing_radius = 35.0;
canal_diameter = 5.0;
bracket_thick  = 3.5;

module semicircular_acoustic_waveguide() {
    difference() {
        // Primary protective shielding chassis
        color("MediumSeaGreen", 0.6)
            sphere(r = housing_radius);
            
        // 3-Axis Fluidic Echo Cavities (Toroidal cutting matrices tracking X, Y, Z coordinates)
        // Axis 1: Horizontal Canal Plane
        rotate([0, 0, 0])
            torus_cut(housing_radius - 8, canal_diameter);
            
        // Axis 2: Anterior Vertical Canal Plane
        rotate([90, 0, 0])
            torus_cut(housing_radius - 8, canal_diameter);
            
        // Axis 3: Posterior Vertical Canal Plane
        rotate([0, 90, 0])
            torus_cut(housing_radius - 8, canal_diameter);
            
        // Center Cavity for the Core Echo-Processor Transceiver Board
        cube([14.0, 14.0, 14.0], center = true);
    }
}

module torus_cut(major_r, minor_r) {
    // Generates localized internal fluid channels for sonic wave routing
    rotate_extrude()
        translate([major_r, 0, 0])
            circle(r = minor_r);
}

module core_alignment_flange() {
    // Standard M4 layout adapter interface locking directly onto the server frame rails
    translate([0, 0, -(housing_radius + bracket_thick / 2 - 2)]) {
        difference() {
            color("DimGray", 1.0)
                cube([housing_radius * 2, 20.0, bracket_thick], center = true);
            // M4 positioning screw tracks
            translate([25, 0, 0]) cylinder(h = 10, r = 2.2, center = true);
            translate([-25, 0, 0]) cylinder(h = 10, r = 2.2, center = true);
        }
    }
}

// System Compilation Assembly
union() {
    semicircular_acoustic_waveguide();
    core_alignment_flange();
}
