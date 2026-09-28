# ====================================================================
# OPENSCAD HEADLESS GEOMETRY COMPILATION TARGETS
# ====================================================================

# OpenSCAD System Path Overrides (Defaulting to Linux mainframe targets)
OPENSCAD = openscad
HARDWARE_DIR = hardware

.PHONY: render-assembly

# Compiles the 3D parametric alignment bracket into a structural manufacturing file
render-assembly: check-env
	@echo "===================================================================="
	@echo "[*] INITIATING HEADLESS OPENSCAD MODEL GENERATION PASS"
	@echo "===================================================================="
	@echo "[*] Ingesting: $(HARDWARE_DIR)/olfactory_chassis_assembly.scad"
	@if ! command -v $(OPENSCAD) &> /dev/null; then \
		echo "[!] CRITICAL COMPILER FAULT: OpenSCAD engine executable not found in system path."; \
		exit 1; \
	fi
	@echo "[*] Executing boolean geometric parsing strings..."
	$(OPENSCAD) -o $(HARDWARE_DIR)/olfactory_chassis_assembly.stl $(HARDWARE_DIR)/olfactory_chassis_assembly.scad
	@echo "[+] MANUFACTURING EXPORT SUCCESSFUL: $(HARDWARE_DIR)/olfactory_chassis_assembly.stl compiled."


# Olfactory verification loop addon target
test-olfactory-intake: check-env
	@echo "===================================================================="
	@echo "[*] LAUNCHING OLFACTORY SPECTROMETER DOCKING SIMULATION"
	@echo "===================================================================="
	@$(PYTHON) src/olfactory_docking_sim.py

# Voxel array serialization compilation hook
voxelize-mesh: render-assembly
	@echo "===================================================================="
	@echo "[*] RUNNING STL VOLUMETRIC TRANSFORMATION COMPILER"
	@echo "===================================================================="
	@$(PYTHON) tools/stl_to_voxel.py

# Kinematic and gaze telemetry test loop hook
test-kinematic-telemetry: check-env
	@echo "===================================================================="
	@echo "[*] RUNNING EXTREMITY KINEMATICS AND GAZE VECTOR PREDICTOR"
	@echo "===================================================================="
	@$(PYTHON) src/telemetry/joint_vector_predictor.py
	@$(PYTHON) src/telemetry/pilot_gaze_tracker.py
