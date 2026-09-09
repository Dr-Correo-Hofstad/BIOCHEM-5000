import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

def generate_spiral_nodes(node_count=150, scaling_factor=4.5, vertical_pitch=0.4):
    """Computes the 3D coordinates of the spiral matrix."""
    golden_angle = np.deg2rad(137.5077)
    indices = np.arange(1, node_count + 1)
    
    angles = indices * golden_angle
    radii = scaling_factor * np.sqrt(indices)
    
    x = radii * np.cos(angles)
    y = radii * np.sin(angles)
    z = indices * vertical_pitch
    
    return x, y, z, indices

def animate_and_save_spiral(output_filename="hardware/helical_interference.mp4"):
    print("[*] Initializing Standing Wave Interference Engine...")
    node_count = 150
    x, y, z, indices = generate_spiral_nodes(node_count=node_count)
    
    # Setup canvas bounds
    fig = plt.figure(figsize=(12, 12), facecolor='black')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')
    ax.set_axis_off()
    
    max_bound = np.max(np.abs([x, y]))
    ax.set_xlim(-max_bound, max_bound)
    ax.set_ylim(-max_bound, max_bound)
    ax.set_zlim(0, np.max(z) + 5)
    
    # Grounding axle trace
    ax.plot([0, 0], [0, 0], [0, np.max(z) + 5], color='gold', alpha=0.3, linewidth=1.0)
    
    scatter = ax.scatter([], [], [], c=[], cmap='bwr', edgecolors='none')
    
    # Wave parameters for interference calculation
    k = 0.20          # Spatial wave number
    omega = 0.25      # Angular frequency
    total_frames = 240
    
    def update_frame(frame):
        nonlocal scatter
        scatter.remove()
        
        # Wave 1: Traveling upward from base node
        wave_up = np.sin(k * indices - omega * frame)
        
        # Wave 2: Traveling downward from top node
        wave_down = np.sin(k * (node_count - indices) - omega * frame)
        
        # Total interference pattern calculation (Superposition Principle)
        interference_pattern = wave_up + wave_down
        
        # Scale sizes based on absolute localized amplitude displacements
        node_sizes = (np.abs(interference_pattern) + 0.2) * 35.0
        
        # Render frame layer with dynamic color tracking
        scatter = ax.scatter(x, y, z, s=node_sizes, c=interference_pattern, cmap='bwr', vmin=-2.0, vmax=2.0)
        
        # Rotational pan configuration
        ax.view_init(elev=20, azim=frame * 1.5)
        return scatter,

    # Configure high-definition video writer metadata
    print(f"[*] Compiling frames into high-definition MP4 profile...")
    writer = animation.FFMpegWriter(fps=30, metadata=dict(artist='BIOCHEM-5000'), bitrate=5000)
    
    ani = animation.FuncAnimation(fig, update_frame, frames=total_frames, blit=False)
    
    # Execute file save routine
    ani.save(output_filename, writer=writer)
    plt.close()
    print(f"[+] Presentation-ready file exported successfully: {output_filename}")

if __name__ == "__main__":
    animate_and_save_spiral()
