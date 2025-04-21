from voice.hotword import wait_for_hotword
from voice.input import listen_until_silence
from voice.output import speak
from gpt.handler import analyze_user_input, summarize_logs
from storage.db import init_db, save_log, get_recent_logs
from openai import OpenAI

print("🎧 포도와 대화를 시작합니다! 가볍게 말 걸어보세요.")
init_db()
client = OpenAI()

while True:
    wait_for_hotword()  # 🔔 "포도야" 감지되면 다음 진행

    audio_buffer = listen_until_silence()
    if audio_buffer is None:
        continue

    text = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_buffer
    ).text

    print(f"📝 인식된 말: {text}")

    if not text.strip():
        continue

    if any(kw in text for kw in ["끝낼게", "여기까지 마무리"]):
        speak("오늘도 수고 많으셨어요. 다음에 또 이야기해요 😊")
        break

    if any(kw in text for kw in ["이번 주 요약", "최근 기록", "일주일 정리"]):
        summaries = get_recent_logs(days=7)
        summary_text = summarize_logs(summaries)
        speak(summary_text)
        continue

    result = analyze_user_input(text)
    speak(f"기록할게요. {result['response']}" if result["should_save"] == "YES" else result["response"])

    if result["should_save"] == "YES":
        save_log(
            raw_text=text,
            summary=result["summary"],
            tags=result.get("tags", []),
            mood=result.get("mood", [])
        )
        print(f"📌 기록 저장됨: {result['summary']} | 태그: {result['tags']} | 분위기: {result['mood']}")
    else:
        print("📝 일반 대화로 저장하지 않았어요.")
