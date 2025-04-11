import uuid
import os
from config import RECORDINGS_DIR


def generate_recording_filename():
    return os.path.join(RECORDINGS_DIR, f"record_{uuid.uuid4().hex[:6]}.wav")
