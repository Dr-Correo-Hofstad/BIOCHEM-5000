// ====================================================================
// DESIGN STANDARDS: RT Helical Structural Engineering Block
// Parametric Fibonacci Spiral and Helical Node Array Generator
// ====================================================================

$fn = 40;

// Golden Ratio Constants
golden_angle = 137.5077;
node_count = 150;
scaling_factor = 4.5;
vertical_pitch = 0.4; // Generates vertical transformation along the Z-axis (Helix)

module generate_fibonacci_spiral_nodes() {
    echo("[*] Computing Fibonacci Helical Coordinates...");
    
    for (i = [1 : node_count]) {
        // Calculate spatial positioning angles using golden rotation
        angle = i * golden_angle;
        // Fermat's Spiral radius calculation: r = c * sqrt(n)
        radius = scaling_factor * sqrt(i);
        
        // Convert polar coordinates to Cartesian coordinates (X, Y, Z)
        pos_x = radius * cos(angle);
        pos_y = radius * sin(angle);
        pos_z = i * vertical_pitch; // Step upwards to form a dimensional spiral
        
        translate([pos_x, pos_y, pos_z]) {
            color("Teal", 1.0 - (i / node_count)) {
                // Spherical nodes mapping the wave path distribution matrix
                sphere(r = 1.8);
                
                // Optional structural anchor link back to the central axial core
                if (i % 5 == 0) {
                    rotate([0, 90, angle])
                        color("DimGray", 0.3)
                            cylinder(h = radius, r = 0.4, center = false);
                }
            }
        }
    }
}

// Instantiate the core spiral array configuration
union() {
    generate_fibonacci_spiral_nodes();
    // Central Grounding Rod Axle
    color("Gold", 0.6)
        cylinder(h = node_count * vertical_pitch + 5, r = 2.0, center = false);
}
