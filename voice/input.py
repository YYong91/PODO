import torch
import numpy as np
import sounddevice as sd
import torchaudio
from voice.hotword import SileroVad
import io
from pydub import AudioSegment

fs = 16000
vad = SileroVad(sample_rate=fs)

def listen_until_silence():
    print("🎧 포도가 말소리를 감지하고 있어요 (silero-vad)...")

    recording = []
    silence_frames = 0
    speaking = False

    stream = sd.InputStream(samplerate=fs, channels=1, dtype='float32', blocksize=512)
    stream.start()

    try:
        while True:
            frame, _ = stream.read(512)  # 약 32ms
            mono = np.squeeze(frame)
            tensor = torch.from_numpy(mono)

            speech_prob = vad(tensor)
            is_speech = speech_prob > 0.5

            if is_speech:
                recording.append(mono)
                silence_frames = 0
                speaking = True
            elif speaking:
                silence_frames += 1
                if silence_frames > 10:  # 약 0.3초 침묵
                    break
    finally:
        stream.stop()
        stream.close()

    if not recording:
        return None

    full_audio = np.concatenate(recording)
    buffer = io.BytesIO()

    audio_segment = AudioSegment(
        data=(full_audio * 32767).astype("int16").tobytes(),
        sample_width=2,
        frame_rate=fs,
        channels=1
    )
    audio_segment.export(buffer, format="wav")
    buffer.seek(0)
    buffer.name = "speech.wav"
    return buffer
