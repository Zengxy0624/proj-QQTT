import os

# .engine (trainer_warp) and camera_system import pynput at module load, which needs an X display.
# Default to :0 when headless (ssh/tmux), respect an existing DISPLAY. Covers every `import qqtt` entry
# point (train/inference/eval), not just process_data.py.
if not os.environ.get("DISPLAY"):
    os.environ["DISPLAY"] = ":0"

from .model import SpringMassSystemWarp
from .engine import InvPhyTrainerWarp, OptimizerCMA
