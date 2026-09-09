import os
import random
import csv
import math
import numpy as np

def execute_batch_seed_simulation(output_csv_path="hardware/batch_simulation_matrix.csv", total_iterations=100):
    """
    Executes a high-volume batch simulation loop across distinct random seeds.
    Tracks, quantizes, and logs X/Y chromosomal drift into a raw tracking ledger.
    """
    print(f"[*] Initializing Multi-Seed Stochastic Run Automation Pipeline...")
    print(f"    - Target Matrix Rows: {total_iterations} Unique Runs")
    
    # Establish CSV logging directory layout
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    
    csv_header = ["run_id", "random_seed", "total_count_millions", "target_y_ratio", "simulated_x_millions", "simulated_y_millions", "y_percentage", "sigma_deviation"]
    
    with open(output_csv_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(csv_header)
        
        for run in range(1, total_iterations + 1):
            # Dynamic runtime parameters to simulate physical population variances
            current_seed = random.randint(100000, 999999)
            random.seed(current_seed)
            np.random.seed(current_seed)
            
            total_count = random.uniform(150.0, 350.0) # Variable sample volumes
            target_p = 0.50
            
            # Normal distribution parameters approximation matching the baseline mathematical core
            n = total_count * 1_000_000
            mean_y = n * target_p
            std_dev_y = math.sqrt(n * target_p * (1 - target_p))
            
            simulated_y = random.gauss(mean_y, std_dev_y)
            simulated_x = n - simulated_y
            
            final_y_percent = (simulated_y / n) * 100
            sigma_dev = abs(simulated_y - mean_y) / std_dev_y
            
            # Write row array data block
            writer.writerow([
                run,
                current_seed,
                round(total_count, 2),
                target_p,
                round(simulated_x / 1_000_000, 4),
                round(simulated_y / 1_000_000, 4),
                round(final_y_percent, 4),
                round(sigma_dev, 4)
            ])
            
    print(f"[+] Stochastic Batch Simulation Complete. Data logged to: {output_csv_path}")

if __name__ == "__main__":
    execute_batch_seed_simulation(total_iterations=50)
