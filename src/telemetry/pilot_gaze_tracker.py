import numpy as np

class PilotGazeTracker:
    def __init__(self):
        # Baseline vector representing the camera coordinate center point
        self.camera_optical_center = np.array([0.0, 0.0, 1.0])

    def calculate_gaze_vector_projection(self, pupil_center_offset_x, pupil_center_offset_y, corneal_reflection_distance):
        """
        Translates raw structural camera inputs into an absolute directional gaze vector.
        """
        print("[*] Parsing Steering Wheel Camera Optoelectronic Feed Array...")
        
        # Construct the look-at orientation vector from pupil offset distances
        raw_gaze_direction = np.array([pupil_center_offset_x, pupil_center_offset_y, corneal_reflection_distance])
        
        # Normalize the vector to extract the unit tracking direction matrix
        magnitude = np.linalg.norm(raw_gaze_direction)
        if magnitude > 0:
            unit_gaze_vector = raw_gaze_direction / magnitude
        else:
            unit_gaze_vector = np.array([0.0, 0.0, 1.0])

        # Map vector coordinate points to screen zones
        horizontal_quadrant = "RIGHT_FIELD" if unit_gaze_vector[0] > 0.05 else ("LEFT_FIELD" if unit_gaze_vector[0] < -0.05 else "CENTER")
        vertical_quadrant = "UPPER_FIELD" if unit_gaze_vector[1] > 0.05 else ("LOWER_FIELD" if unit_gaze_vector[1] < -0.05 else "CENTER")

        print(f"    [+] Gaze Coordinates Locked:")
        print(f"        - Target Unit Direction Matrix: [{unit_gaze_vector[0]:.4f}, {unit_gaze_vector[1]:.4f}, {unit_gaze_vector[2]:.4f}]")
        print(f"        - Identified Focus Quadrant   : [{horizontal_quadrant} | {vertical_quadrant}]\n")
        
        return unit_gaze_vector

if __name__ == "__main__":
    tracker = PilotGazeTracker()
    # Simulate pilot scanning up and to the right quadrant field
    tracker.calculate_gaze_vector_projection(pupil_center_offset_x=0.18, pupil_center_offset_y=0.22, corneal_reflection_distance=0.95)
