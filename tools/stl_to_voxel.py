import os
import struct
import numpy as np

class STLToVoxelConverter:
    def __init__(self, stl_path, resolution_grid=32):
        self.stl_path = stl_path
        self.grid_res = resolution_grid

    def parse_binary_stl_facets(self):
        """Reads and unpacks the raw 3D coordinate vertices from a binary STL file."""
        if not os.path.exists(self.stl_path):
            raise FileNotFoundError(f"Source geometry mesh not found: {self.stl_path}")

        print(f"[*] Extracting polygon arrays from: {self.stl_path}")
        triangles = []
        
        with open(self.stl_path, 'rb') as f:
            header = f.read(80) # Skip standard 80-byte header
            num_triangles = struct.unpack('<I', f.read(4))[0]
            
            for _ in range(num_triangles):
                # Unpack Normal vector (3 floats), Vertices 1-3 (9 floats), and attribute byte count (1 uint16)
                data = struct.unpack('<ffffffffffffH', f.read(50))
                v1 = (data[3], data[4], data[5])
                v2 = (data[6], data[7], data[8])
                v3 = (data[9], data[10], data[11])
                triangles.append((v1, v2, v3))
                
        return np.array(triangles)

    def convert_mesh_to_3d_density_grid(self, voxel_out_path="hardware/voxel_matrix.bin"):
        """Converts the parsed 3D polygon array into a volumetric binary density grid."""
        facets = self.parse_binary_stl_facets()
        print(f"[*] Re-indexing space into a [{self.grid_res}^3] voxel density matrix...")
        
        # Calculate bounding envelope metrics
        flat_vertices = facets.reshape(-1, 3)
        min_bounds = flat_vertices.min(axis=0)
        max_bounds = flat_vertices.max(axis=0)
        
        # Initialize an empty volumetric byte grid map (0 = Vacuum space, 1 = Dense Solid Hull)
        voxel_grid = np.zeros((self.grid_res, self.grid_res, self.grid_res), dtype=np.uint8)
        
        # Basic volumetric voxel checker tracking centroid intersection
        # Coordinates map straight into Metastasis-Tracker-AI array configurations
        grid_steps = (max_bounds - min_bounds) / self.grid_res
        
        for idx_x in range(self.grid_res):
            for idx_y in range(self.grid_res):
                # Calculate sample tracking ray vectors across coordinate cross-sections
                coord_x = min_bounds[0] + (idx_x + 0.5) * grid_steps[0]
                coord_y = min_bounds[1] + (idx_y + 0.5) * grid_steps[1]
                
                # Fast voxel field estimation loop based on vertex height maps
                for facet in facets:
                    f_min_x, f_max_x = min(facet[:,0]), max(facet[:,0])
                    f_min_y, f_max_y = min(facet[:,1]), max(facet[:,1])
                    
                    if (f_min_x <= coord_x <= f_max_x) and (f_min_y <= coord_y <= f_max_y):
                        # Approximate depth fill
                        mean_z = int(((facet[:,2].mean() - min_bounds[2]) / grid_steps[2]))
                        z_index = max(0, min(self.grid_res - 1, mean_z))
                        voxel_grid[idx_x, idx_y, z_index] = 1

        # Commit binary voxel file straight to disk for neural tracking loops
        os.makedirs(os.path.dirname(voxel_out_path), exist_ok=True)
        with open(voxel_out_path, 'wb') as out_f:
            out_f.write(voxel_grid.tobytes())
            
        print(f"[+] VOXELIZATION TIMELINE FINALIZED: 3D density block saved to: {voxel_out_path}")
        return voxel_grid

if __name__ == "__main__":
    converter = STLToVoxelConverter(stl_path="hardware/olfactory_chassis_assembly.stl", resolution_grid=32)
    try:
        converter.convert_mesh_to_3d_density_grid()
    except FileNotFoundError as err:
        print(f"[!] Compilation Bypassed: {err}. Execute 'make render-assembly' first.")
