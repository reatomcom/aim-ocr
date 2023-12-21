import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).absolute().parent


def rel2abs(path):
    path = Path(path)
    return path if path.is_absolute() else PROJECT_ROOT.joinpath(path)


DATASET_DIR = rel2abs(os.environ["DATASET_DIR"])
OUTPUT_DIR = rel2abs(os.environ["OUTPUT_DIR"])
