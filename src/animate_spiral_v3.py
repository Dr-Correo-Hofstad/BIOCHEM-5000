import os
import csv
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

def isolate_and_log_null_nodes(x, y, z, indices, k, node_count, csv_path="hardware/null_nodes_ledger.csv"):
    """
    Identifies the permanent spatial null points where the standing wave 
    envelope cross-over zeroes out, and logs coordinates to a CSV ledger.
    """
    print(f"[*] Analyzing spatial wave envelopes to isolate null nodes...")
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    
    # Calculate the time-independent spatial amplitude factor for each node
    spatial_factor = np.cos(k * indices - (k * node_count) / 2.0)
    
    # A node is a local minimum of the absolute spatial factor (closest to zero)
    # Or where it crosses/touches zero. We filter for high-attenuation boundaries:
    null_threshold = 0.15  # Tolerance for proximity to absolute null state
    
    null_nodes_logged = 0
    
    with open(csv_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["null_node_index", "node_id", "coord_x", "coord_y", "coord_z", "attenuation_factor"])
        
        for idx in range(len(indices)):
            if np.abs(spatial_factor[idx]) < null_threshold:
                null_nodes_logged += 1
                writer.writerow([
                    null_nodes_logged,
                    indices[idx],
                    round(x[idx], 4),
                    round(y[idx], 4),
                    round(z[idx], 4),
                    round(float(np.abs(spatial_factor[idx])), 6)
                ])
                
    print(f"[+] Destructive interference matrix logged. {null_nodes_logged} nodes written to: {csv_path}")
    return null_threshold

def animate_and_save_spiral(output_filename="hardware/helical_interference.mp4"):
    print("[*] Initializing Standing Wave Interference Engine...")
    node_count = 150
    scaling_factor = 4.5
    vertical_pitch = 0.4
    x, y, z, indices = generate_spiral_nodes(node_count=node_count, scaling_factor=scaling_factor, vertical_pitch=vertical_pitch)
    
    # Wave parameters
    k = 0.20          # Spatial wave number
    omega = 0.25      # Angular frequency
    total_frames = 240
    
    # Isolate and log the null nodes before compilation
    isolate_and_log_null_nodes(x, y, z, indices, k, node_count)
    
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
    ax.plot(,, [0, np.max(z) + 5], color='gold', alpha=0.3, linewidth=1.0)
    
    scatter = ax.scatter([], [], [], c=[], cmap='bwr', edgecolors='none')
    
    def update_frame(frame):
        nonlocal scatter
        scatter.remove()
        
        wave_up = np.sin(k * indices - omega * frame)
        wave_down = np.sin(k * (node_count - indices) - omega * frame)
        interference_pattern = wave_up + wave_down
        
        node_sizes = (np.abs(interference_pattern) + 0.2) * 35.0
        scatter = ax.scatter(x, y, z, s=node_sizes, c=interference_pattern, cmap='bwr', vmin=-2.0, vmax=2.0)
        
        ax.view_init(elev=20, azim=frame * 1.5)
        return scatter,

    print(f"[*] Compiling frames into high-definition MP4 profile...")
    writer = animation.FFMpegWriter(fps=30, metadata=dict(artist='BIOCHEM-5000'), bitrate=5000)
    ani = animation.FuncAnimation(fig, update_frame, frames=total_frames, blit=False)
    ani.save(output_filename, writer=writer)
    plt.close()
    print(f"[+] Presentation-ready video exported successfully: {output_filename}")

if __name__ == "__main__":
    animate_and_save_spiral()
