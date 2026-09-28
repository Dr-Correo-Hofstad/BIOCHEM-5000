import numpy as np
import math

class OlfactorySpectrometer:
    def __init__(self, target_nodes=16):
        # Establishes positively charged amino-acid receptor reference vector lines
        # Represents the static hardware receiver grid matrix
        self.receptor_charge_matrix = np.random.uniform(0.5, 1.5, (target_nodes, 3))
        # Normalize baseline target matrices
        norms = np.linalg.norm(self.receptor_charge_matrix, axis=1, keepdims=True)
        self.receptor_charge_matrix /= norms

    def simulate_odorant_docking(self, compound_name, dipole_moment_debye, dipole_vector_xyz):
        """
        Calculates the torque alignment and charge release value of an odorant 
        molecule colliding with the electrostatic sensor pad.
        """
        print(f"[*] Ingesting Gas-Phase Chemical Signature: {compound_name}")
        
        # Verify if compound lacks dipole polarity (making it inherently odorless)
        if dipole_moment_debye == 0.0:
            print(f"    [-] Compound '{compound_name}' lacks a dipole moment. Vector is inert / Odorless.")
            return {"voltage_output_mv": 0.0, "alignment_accuracy": 0.0}

        # Convert input tuple to normalized numpy vector representation
        d_vec = np.array(dipole_vector_xyz, dtype=float)
        if np.linalg.norm(d_vec) > 0:
            d_vec /= np.linalg.norm(d_vec)

        # Compute dot-product matrix cross-sections (Torque alignment check)
        # Reflects how a molecule aligns its negative charge surface to the positive pads
        alignment_scores = np.dot(self.receptor_charge_matrix, d_vec)
        best_match_idx = np.argmax(alignment_scores)
        max_alignment = float(alignment_scores[best_match_idx])

        # Electrochemical Conversion Formula: V = q * d * cos(theta) * efficiency
        # Steps up the chemical recognition into an active cellular neural pulse potential
        conversion_efficiency = 45.0  # Scalar optimization coefficient
        induced_voltage_mv = max_alignment * dipole_moment_debye * conversion_efficiency

        print(f"    [+] Electrostatic Alignment Achieved on Card Slot Node #{best_match_idx}")
        print(f"    - Dipole Magnitude  : {dipole_moment_debye:.4f} Debye")
        print(f"    - Alignment Accuracy: {max_alignment*100:.2f}% Match")
        print(f"    - Induced Signal Bus Potential: {induced_voltage_mv:.4f} mV DC\n")

        return {
            "voltage_output_mv": induced_voltage_mv,
            "alignment_accuracy": max_alignment,
            "matched_receptor_node": best_match_idx
        }

if __name__ == "__main__":
    spectrometer = OlfactorySpectrometer()

    # Case 1: Odorous Polar Compound (e.g., Vanillin variant trace)
    spectrometer.simulate_odorant_docking(
        compound_name="Vanillin_Analog_09",
        dipole_moment_debye=3.12,
        dipole_vector_xyz=[0.81, -0.42, 0.41]
    )

    # Case 2: Inert Non-Polar Gas (e.g., Pure Nitrogen/Hydrogen baseline check)
    spectrometer.simulate_odorant_docking(
        compound_name="Inert_Carrier_Gas_N2",
        dipole_moment_debye=0.0,
        dipole_vector_xyz=[0.0, 0.0, 0.0]
    )
