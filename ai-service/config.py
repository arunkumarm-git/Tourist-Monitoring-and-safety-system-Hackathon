import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
MODELS_DIR = BASE_DIR / "models"
ZONES_PATH = MODELS_DIR / "zones.json"

EPSILON_METERS = int(os.getenv("EPSILON_METERS", "50"))
MIN_SAMPLES = int(os.getenv("MIN_SAMPLES", "8"))

HOST = os.getenv("AI_HOST", "0.0.0.0")
PORT = int(os.getenv("AI_PORT", "8001"))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")