import json
import math
import os

def calculate_null_nodes(node_count=150, k=0.20, threshold=0.15):
    """Calculates which node indices drop below the attenuation threshold for a given k."""
    indices = np.arange(1, node_count + 1) if 'np' in globals() else list(range(1, node_count + 1))
    null_indices = []
    
    for i in indices:
        # Spatial factor envelope equation matching the standing wave model
        spatial_factor = math.cos(k * i - (k * node_count) / 2.0)
        if abs(spatial_factor) < threshold:
            null_indices.append(i)
            
    return null_indices

def run_wave_shift_verification():
    print("[*] Launching Spatial Wave Number Verification Routine...")
    node_count = 150
    threshold = 0.15
    scaling_factor = 4.5
    vertical_pitch = 0.4
    golden_angle = math.radians(137.5077)
    
    # Range of spatial wave numbers (k) to analyze
    k_vals = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40]
    
    print("--- Sensitivity Analysis: k-Shift vs. Null Node Trapping Count ---")
    for k in k_vals:
        active_nulls = calculate_null_nodes(node_count, k, threshold)
        print(f"  - Spatial Wave Number (k): {k:.2f} | Trapped Null Nodes: {len(active_nulls)}")
        
    # Export the standard baseline configuration (k=0.20) to JSON for OpenSCAD parsing
    baseline_k = 0.20
    baseline_nulls = calculate_null_nodes(node_count, baseline_k, threshold)
    
    # Structure node array data payload
    json_payload = {"null_node_ids": baseline_nulls}
    
    json_path = "hardware/null_nodes.json"
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    with open(json_path, 'w') as f:
        json.dump(json_payload, f, indent=2)
        
    print(f"\n[+] Baseline data exported successfully to: {json_path}")

if __name__ == "__main__":
    run_wave_shift_verification()
