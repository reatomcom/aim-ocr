import os
import main
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = os.path.dirname(os.path.abspath(main.__file__))
DATASET_PATH = (lambda x: x if os.path.isabs(x) else os.path.join(PROJECT_ROOT, x))(
    os.environ["DATASET_PATH"]
)
