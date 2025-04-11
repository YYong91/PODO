import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 175)  # 말 속도 조절


def speak(text):
    print("🗣️ 포도:", text)
    engine.say(text)
    engine.runAndWait()
