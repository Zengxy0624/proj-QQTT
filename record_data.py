from datetime import datetime
from qqtt.env import CameraSystem
import os

def exist_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

if __name__ == "__main__":
    camera_system = CameraSystem()
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    exist_dir(f"data_collect")
    camera_system.record(
        output_path=f"data_collect/{current_time}"
    )
    # Copy the camera calibration file to the output path
    os.system(
        f"cp calibrate.pkl data_collect/{current_time}"
    )
