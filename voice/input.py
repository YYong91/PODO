import sounddevice as sd
import scipy.io.wavfile as wav
from keyboard import stop_recording
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


def record_until_enter(filename):
    global recording, stream
    recording = []

    def callback(indata, frames, time_info, status):
        recording.append(indata.copy())

    def on_press(key):
        nonlocal is_recording
        if key == keyboard.Key.enter:
            if not is_recording:
                print("🎙️ 녹음 시작...")
                is_recording = True
                stream.start()
            else:
                print("⏹️ 녹음 종료")
                stream.stop()
                return False  # 리스너 종료

    is_recording = False

    stream = sd.InputStream(samplerate=fs, channels=1, dtype='int16', callback=callback)
    print("⏺️ 엔터 누르면 녹음 시작 → 다시 엔터 누르면 종료됩니다.")

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    all_data = np.concatenate(recording, axis=0)
    wav.write(filename, fs, all_data)
    print("✅ 녹음 저장 완료:", filename)


def transcribe(filename):
    with open(filename, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    print("📝 인식된 텍스트:", transcript.text)
    return transcript.text
