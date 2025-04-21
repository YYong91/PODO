import os
from dotenv import load_dotenv

load_dotenv()

RECORDINGS_DIR = "recordings"
DB_PATH = "data/growth_log.db"
BABY_NAME = os.getenv("BABY_NAME", "아기")

os.makedirs(RECORDINGS_DIR, exist_ok=True)
os.makedirs("data", exist_ok=True)
