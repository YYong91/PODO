import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 175)


def speak(text, prefix="포도"):
    print(f"🗣️ {prefix}: {text}")
    engine.say(text)
    engine.runAndWait()
