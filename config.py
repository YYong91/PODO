import os

RECORDINGS_DIR = "recordings"
DB_PATH = "data/growth_log.db"

# 디렉토리 자동 생성
os.makedirs(RECORDINGS_DIR, exist_ok=True)
os.makedirs("data", exist_ok=True)
