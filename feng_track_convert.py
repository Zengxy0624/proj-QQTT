import numpy as np
import pickle

DATA_PATH = "data/feng_version/feng_rope_v6_0001_feng_track"
FENG_TRACK_PATH = f"{DATA_PATH}/feng_track.npz"
ORIGINAL_TRACK_PATH = f"{DATA_PATH}/track_process_data_original.pkl"

FINAL_TRACK_PATH = f"{DATA_PATH}/track_process_data.pkl"

start_frame = 164
end_frame = 1000

if __name__ == "__main__":
    # Read the FENG_TRACK_PATH
    feng_track = np.load(FENG_TRACK_PATH)
    points_feng = feng_track["xyz"]
    # Read the ORIGINAL_TRACK_PATH
    with open(ORIGINAL_TRACK_PATH, "rb") as f:
        track_data = pickle.load(f)

    # Interpolate the points_feng to 2x, interpolate one point between two adjacent points
    points_feng_interpolated = np.zeros(
        (points_feng.shape[0] * 2 - 1, points_feng.shape[1], 3)
    )
    cur_index = 0
    for i in range(points_feng.shape[0]):
        points_feng_interpolated[cur_index] = points_feng[i]
        cur_index += 1
        if i < points_feng.shape[0] - 1:
            points_feng_interpolated[cur_index] = (
                points_feng[i] + points_feng[i + 1]
            ) / 2
            cur_index += 1
    new_points = points_feng_interpolated[start_frame : end_frame + 1]

    new_visibilities = np.ones((new_points.shape[0], new_points.shape[1]), dtype=bool)
    new_motions_valid = np.ones((new_points.shape[0], new_points.shape[1]), dtype=bool)
    new_motions_valid[-1] = 0
    new_colors = np.zeros((new_points.shape[0], new_points.shape[1], 3))

    track_data["object_points"] = new_points
    track_data["object_visibilities"] = new_visibilities
    track_data["object_motions_valid"] = new_motions_valid
    track_data["object_colors"] = new_colors

    # Save the track_data to the ORIGINAL_TRACK_PATH
    with open(FINAL_TRACK_PATH, "wb") as f:
        pickle.dump(track_data, f)