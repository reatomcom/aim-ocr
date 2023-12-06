import os
from pathlib import Path

from dotenv import load_dotenv

import main

load_dotenv()

PROJECT_ROOT = Path(main.__file__).absolute().parent


def rel2abs(path):
    return path if path.is_absolute() else PROJECT_ROOT.joinpath(path)


DATASET_PATH = rel2abs(Path(os.environ["DATASET_PATH"]))
