import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent

FIREBASE_CREDS_PATH = os.getenv("FIREBASE_CREDS_PATH", "firebase-creds.json")
FIREBASE_DATABASE_URL = os.getenv("FIREBASE_DATABASE_URL")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

AI_SERVICE_URL = os.getenv("AI_SERVICE_URL", "http://localhost:8001")

SECRET_KEY = os.getenv("SECRET_KEY")

HOST = os.getenv("BACKEND_HOST", "0.0.0.0")
PORT = int(os.getenv("BACKEND_PORT", "5000"))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

ANOMALY_CHECK_INTERVAL = int(os.getenv("ANOMALY_CHECK_INTERVAL", "10"))
