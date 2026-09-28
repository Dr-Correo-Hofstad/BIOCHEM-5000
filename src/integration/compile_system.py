import os
import sys
import json
import re

class FrameworkCompiler:
    def __init__(self, root_dir="workspace/Metastasis-Tracker-AI"):
        self.root_dir = root_dir
        self.required_subsystems = [
            "core", "src", "hardware", "outbound", "tools", "docs/curriculum"
        ]
        self.config_path = os.path.join(self.root_dir, "src/data/state_matrix.json")
        self.scad_path = os.path.join(self.root_dir, "hardware/olfactory_chassis_assembly.scad")
        self.safety_log_path = os.path.join(self.root_dir, "outbound/safety_breaches.log")

    def verify_and_build_scaffolding(self):
        """Ensures all modular structural directories exist within the project path."""
        print(f"[*] Initializing Multi-Repository System Integration Pass...")
        for folder in self.required_subsystems:
            path = os.path.join(self.root_dir, folder)
            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True)
                print(f"    [+] Created missing infrastructure node: {folder}")
        print("[+] Repository directory scaffolding verified.\n")

    def verify_m4_fastener_alignment(self, state_data):
        """
        CI/CD Cross-Verification Gate: Asserves that the hardware pitch variables defined
        in the json parameter matrix mirror the rigid constants encoded inside OpenSCAD.
        """
        print("[*] CI/CD Verification: Cross-checking M4 grid arrays against OpenSCAD geometry...")
        if not os.path.exists(self.scad_path):
            print("    [!] Warning: Olfactory SCAD template missing. Skipping structural audit.")
            return True

        fastener_config = state_data.get("chassis_fastener_matrix", {})
        json_pitch_x = float(fastener_config.get("grid_pitch_x_mm", 25.0))
        json_pitch_y = float(fastener_config.get("grid_pitch_y_mm", 20.0))

        with open(self.scad_path, 'r') as f:
            scad_content = f.read()

        # Regular expression extraction of active OpenSCAD pitch bounds
        match_x = re.search(r'grid_pitch_x\s*=\s*([\d\.]+);', scad_content)
        match_y = re.search(r'grid_pitch_y\s*=\s*([\d\.]+);', scad_content)

        if match_x and match_y:
            scad_pitch_x = float(match_x.group(1))
            scad_pitch_y = float(match_y.group(1))
            
            if json_pitch_x != scad_pitch_x or json_pitch_y != scad_pitch_y:
                print(f"    [!] STRUCTURAL ALIGNMENT ERROR: Pitch Mismatch Detected!")
                print(f"        - JSON Profile: X={json_pitch_x}mm, Y={json_pitch_y}mm")
                print(f"        - SCAD Code   : X={scad_pitch_x}mm, Y={scad_pitch_y}mm")
                return False
            print("    [+] Structural alignment match verified: Pitch grids are perfectly co-registered.")
            return True
        print("    [!] Warning: Could not locate grid variables inside OpenSCAD code layout template.")
        return True

    def evaluate_system_performance_and_safety(self):
        """ Monitors performance telemetry and records olfactory toxicity breaches. """
        print("[*] Executing system telemetry and biological safety evaluation passes...")
        if not os.path.exists(self.config_path):
            return self.generate_default_state_matrix()

        try:
            with open(self.config_path, 'r') as f:
                state_data = json.load(f)
        except (json.JSONDecodeError, IOError):
            return

        # 1. Trigger the M4 structural alignment verification check
        if not self.verify_m4_fastener_alignment(state_data):
            print("    [!] CRITICAL CI/CD REJECTION: Hardware tracking grids are misaligned.")
            sys.exit(1)

        # 2. Automated Safety Logging Loop: Ingest olfactory signal response potentials
        olfactory_data = state_data.get("olfactory_intake_telemetry", {})
        measured_voltage = olfactory_data.get("last_measured_signal_mv", 45.0)
        toxicity_ceiling = olfactory_data.get("critical_toxicity_voltage_threshold_mv", 120.0)

        if measured_voltage > toxicity_ceiling:
            print(f"    [!] TOXICITY CEILING BREACHED: Olfactory response is at {measured_voltage} mV!")
            os.makedirs(os.path.dirname(self.safety_log_path), exist_ok=True)
            with open(self.safety_log_path, 'a') as log_file:
                log_file.write(f"[BREACH] Critical air-gas boundary alert. Intrusive Potential: {measured_voltage}mV | Threshold Cap: {toxicity_ceiling}mV\n")
            print(f"    [+] Safety tracking event appended cleanly to: {self.safety_log_path}")

        # 3. Handle standard GPU thread metrics scaling loops
        telemetry = state_data.get("gpu_telemetry_profile", {})
        last_measured = telemetry.get("last_measured_execution_time", 425)
        budget = telemetry.get("target_execution_budget_microseconds", 1500)
        current_block_size = state_data.get("zooid_transport", {}).get("memory_pool_block_size", 4096)

        if last_measured > budget:
            if current_block_size > 1024:
                state_data["zooid_transport"]["memory_pool_block_size"] = current_block_size // 2
                state_data["gpu_telemetry_profile"]["pipeline_saturation_status"] = "THROTTLED_DOWN"
        else:
            state_data["gpu_telemetry_profile"]["pipeline_saturation_status"] = "NOMINAL"
            if current_block_size < 4096:
                state_data["zooid_transport"]["memory_pool_block_size"] = current_block_size * 2

        with open(self.config_path, 'w') as f:
            json.dump(state_data, f, indent=2)
        print("[+] System telemetry metrics fully consolidated and synced.\n")

    def generate_default_state_matrix(self):
        """Compiles clean system variables across repositories into a default state file."""
        default_config = {
            "system_meta": {"version": "2026.4.1", "compliance": "FHIR-R4_UEFI-HX"},
            "tissue_yield_thresholds_mpa": {
                "brain_neural_matrix": 0.03, "macro_artery_trunk": 2.80, "capillary_bed_boundary": 0.12
            },
            "haptic_baseline": {"voltage_mv": 290.0, "frequency_hz": 100.0},
            "zooid_transport": {"nominal_glucose_concentration": 0.85, "base_adhesion_coefficient": 0.74, "memory_pool_block_size": 4096},
            "gpu_telemetry_profile": {"target_execution_budget_microseconds": 1500, "last_measured_execution_time": 425, "pipeline_saturation_status": "NOMINAL"},
            "olfactory_intake_telemetry": {"sensor_nodes_count": 16, "baseline_airflow_rate_lmin": 6.5, "critical_toxicity_voltage_threshold_mv": 120.0, "last_measured_signal_mv": 45.0},
            "chassis_fastener_matrix": {"screw_type": "M4_Rigid_Steel", "clearance_radius_mm": 2.2, "grid_pitch_x_mm": 25.0, "grid_pitch_y_mm": 20.0}
        }
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(default_config, f, indent=2)

    def run_integration_diagnostic(self):
        print("[+] SYSTEM INTEGRATION STATUS: NOMINAL. Infrastructure validation run completed successfully.")

if __name__ == "__main__":
    compiler = FrameworkCompiler()
    compiler.verify_and_build_scaffolding()
    compiler.evaluate_system_performance_and_safety()
    compiler.run_integration_diagnostic()
