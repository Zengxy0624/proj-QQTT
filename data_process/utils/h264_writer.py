import subprocess

import numpy as np


class H264VideoWriter:
    """Drop-in for cv2.VideoWriter that pipes BGR uint8 frames to the system ffmpeg's
    libx264. pip opencv-python ships an ffmpeg without libx264, so its H.264 VideoWriter
    falls back to an absent hardware encoder (h264_v4l2m2m) and fails; mp4v works but is
    not playable in browsers / VS Code. This yields a real H.264 mp4. Finalizes on
    .release() or on garbage collection, matching cv2.VideoWriter's behavior."""

    def __init__(self, path, fps, width, height):
        self._proc = subprocess.Popen(
            ["ffmpeg", "-y", "-loglevel", "error",
             "-f", "rawvideo", "-pix_fmt", "bgr24",
             "-s", f"{int(width)}x{int(height)}", "-r", str(int(fps)), "-i", "-",
             "-c:v", "libx264", "-pix_fmt", "yuv420p", path],
            stdin=subprocess.PIPE,
        )

    def write(self, frame):
        self._proc.stdin.write(np.ascontiguousarray(frame, dtype=np.uint8).tobytes())

    def release(self):
        if self._proc is not None:
            self._proc.stdin.close()
            self._proc.wait()
            self._proc = None

    def __del__(self):
        try:
            self.release()
        except Exception:
            pass
