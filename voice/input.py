import sounddevice as sd
import scipy.io.wavfile as wav
from openai import OpenAI
from dotenv import load_dotenv
from pynput import keyboard
import os
import uuid
import numpy as np
import threading

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

recording = []
stream = None
fs = 44100
filename = f"record_{uuid.uuid4().hex[:6]}.wav"


def start_recording():
    global recording, stream
    print("🎙️ 녹음 시작")
    recording = []

    def callback(indata, frames, time_info, status):
        recording.append(indata.copy())

    stream = sd.InputStream(samplerate=fs, channels=1, dtype='int16', callback=callback)
    stream.start()


def stop_recording():
    global stream
    print("⏹️ 녹음 종료")
    stream.stop()

    all_data = np.concatenate(recording, axis=0)
    wav.write(filename, fs, all_data)
    return filename


def transcribe(file):
    with open(file, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    print("📝 인식된 텍스트:", transcript.text)
    return transcript.text


def on_press(key):
    global is_recording
    if key == keyboard.Key.enter:
        if not is_recording:
            is_recording = True
            threading.Thread(target=start_recording).start()
        else:
            is_recording = False
            file = stop_recording()
            transcribe(file)
            return False  # 키 리스너 종료


if __name__ == "__main__":
    print("⏺️ 엔터 누르면 녹음 시작 → 다시 엔터 누르면 종료")
    is_recording = False
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
