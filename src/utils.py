import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

TRAIN_FOLDER = BASE_DIR / "data" / "train"
TEST_FOLDER = BASE_DIR / "data" / "test"

TRAIN_CSV = BASE_DIR / "data" / "train.csv"
TEST_CSV = BASE_DIR / "data" / "test.csv"

MODEL_DIR = BASE_DIR / "models"
OUTPUT_DIR = BASE_DIR / "outputs"

MODEL_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)