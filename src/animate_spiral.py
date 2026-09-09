import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

def generate_spiral_nodes(node_count=150, scaling_factor=4.5, vertical_pitch=0.4):
    """
    Computes the static 3D Cartesian coordinates of the Fibonacci Helical Array
    matching the structural parameters of the OpenSCAD module layout.
    """
    golden_angle = np.deg2rad(137.5077)
    indices = np.arange(1, node_count + 1)
    
    # Calculate angular rotation and Fermat's radius rules
    angles = indices * golden_angle
    radii = scaling_factor * np.sqrt(indices)
    
    # Map out the 3D coordinate matrices
    x = radii * np.cos(angles)
    y = radii * np.sin(angles)
    z = indices * vertical_pitch
    
    return x, y, z, indices

def animate_wave_propagation():
    print("[*] Compiling Spatiotemporal Helical Array Animation Engine...")
    
    # Extract structural baseline coordinates
    node_count = 150
    x, y, z, indices = generate_spiral_nodes(node_count=node_count)
    
    # Initialize multi-axis visualization canvas
    fig = plt.figure(figsize=(10, 8), facecolor='black')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')
    
    # Deactivate grid and axis planes for optimal high-contrast clarity
    ax.grid(False)
    ax.w_xaxis.pane.fill = False
    ax.w_yaxis.pane.fill = False
    ax.w_zaxis.pane.fill = False
    ax.set_axis_off()
    
    # Set structural tracking view bounds
    max_bound = np.max(np.abs([x, y]))
    ax.set_xlim(-max_bound, max_bound)
    ax.set_ylim(-max_bound, max_bound)
    ax.set_zlim(0, np.max(z) + 5)
    
    # Render static center grounding axle rod
    ax.plot([0, 0], [0, 0], [0, np.max(z) + 5], color='gold', alpha=0.4, linewidth=1.5)
    
    # Initialize empty scatter element for dynamic runtime modification
    scatter = ax.scatter([], [], [], c=[], cmap='coolwarm', edgecolors='none')
    
    def update_frame(frame):
        # Time-variable wave function: W(x, t) = A * sin(k*x - omega*t)
        # Propagates a spatial voltage frequency up the index array over time
        wave_frequency = 0.15
        propagation_speed = 0.2
        wave_amplitude = np.sin(indices * wave_frequency - frame * propagation_speed)
        
        # Map localized scalar intensities to node sizing arrays
        # Normalizes sizes to ensure visibility while accentuating peak voltage states
        node_sizes = (wave_amplitude + 1.1) * 20.0
        
        # Clear previous frame updates
        nonlocal scatter
        scatter.remove()
        
        # Re-render dynamic frame layer with updated color intensity maps (C-bus mapping)
        scatter = ax.scatter(x, y, z, s=node_sizes, c=wave_amplitude, cmap='coolwarm', vmin=-1.0, vmax=1.0)
        
        # Rotate camera coordinates smoothly to showcase the 3D lattice dimensions
        ax.view_init(elev=25, azim=frame * 0.4)
        return scatter,

    # Construct the continuous looping animation sequence (30 FPS performance target)
    ani = animation.FuncAnimation(fig, update_frame, frames=300, interval=33, blit=False)
    
    print("[+] System Active. Displaying real-time wave tracking up the spiral...")
    plt.show()

if __name__ == "__main__":
    animate_wave_propagation()
