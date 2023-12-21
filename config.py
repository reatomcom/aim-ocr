import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).absolute().parent


def rel2abs(path: Path):
    return path if path.is_absolute() else PROJECT_ROOT.joinpath(path)


for path_env_var in ("DATASET_DIR", "OUTPUT_FILE"):
    globals()[path_env_var] = rel2abs(Path(os.environ[path_env_var]))
