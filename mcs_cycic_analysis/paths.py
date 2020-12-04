from pathlib import Path

ROOT_DIR_PATH = Path(__file__).parent.parent
DATA_DIR_PATH = ROOT_DIR_PATH / "data"
assert DATA_DIR_PATH.is_dir(), DATA_DIR_PATH
