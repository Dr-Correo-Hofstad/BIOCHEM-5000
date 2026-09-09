# BIOCHEM-5000: Parametric Helical Architectures and Stochastic Gamete Simulators

This repository hosts the structural engineering models, data parameters, and stochastic simulation pipelines mapping out biological geometries and cell-sorting distributions. 

## 1. System Framework Overview
The project is divided into two primary analytical pipelines:
1. **Biomedical Spatial Infrastructure (`hardware/`):** A data-driven 3D layout of anatomical clearance zones and helical structures. It imports parameters directly from a JSON configuration matrix to scale physical design bounds dynamically.
2. **Stochastic Sorting Analysis (`src/`):** A batch processing simulation engine that calculates X vs. Y chromosomal sorting distributions across multiple randomized seeds, exporting full tracking matrices to a standard `.csv` log.

[ pelvic_dimensions.json ]\
│\
▼\
[ pelvic_cavity_mapping.scad ] ──► Compiles 3D Clearance Geometry\
[ spiral_helical_array.scad ] ──► Renders Golden Spiral Node Paths

## 2. File Directory Map
* `hardware/pelvic_dimensions.json` - Core data array containing geometric widths, depths, and offsets.
* `hardware/pelvic_cavity_mapping.scad` - Elliptical boundary tracking file utilizing the JSON data matrix.
* `hardware/spiral_helical_array.scad` - Parametric Fibonacci spiral generator for structural energy distribution.
* `src/chromosomal_probability.py` - Single-run Gaussian approximation simulator for gamete distribution.
* `src/plot_sperm_bell_curve.py` - Python script rendering the high-resolution Probability Density Function (PDF).
* `src/batch_seed_runner.py` - Multi-seed automation loop exporting data logs to CSV.

## 3. Dependency Configuration
To execute these files locally, establish a standard scientific environment:
```bash
pip install numpy matplotlib scipy pandas
```
To render the OpenSCAD geometries dynamically from the JSON file, ensure you are utilizing **OpenSCAD v2021.01 or later** with the experimental JSON feature enabled.
