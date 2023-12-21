import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).absolute().parent


def rel2abs(path):
    path = Path(path)
    return path if path.is_absolute() else PROJECT_ROOT.joinpath(path)


for path_env_var in ("DATASET_DIR", "OUTPUT_DIR", "OUTPUT_FILE"):
    globals()[path_env_var] = rel2abs(os.environ[path_env_var])
