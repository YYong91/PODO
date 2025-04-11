import os
from dotenv import load_dotenv

RECORDINGS_DIR = "recordings"
os.makedirs(RECORDINGS_DIR, exist_ok=True)

DB_PATH = "data/growth_log.db"
os.makedirs("data", exist_ok=True)
load_dotenv()
BABY_NAME = os.getenv("BABY_NAME", "아기")
