from voice.input import record_until_enter, transcribe
from voice.output import speak
from gpt.handler import get_gpt_response
from storage.db import init_db, save_log
from gpt.handler import get_log_summary_or_none
import os
import uuid

# 앱 시작 시 초기화
os.makedirs("recordings", exist_ok=True)
os.makedirs("data", exist_ok=True)
init_db()

if __name__ == "__main__":
    print("🍇 포도와 대화를 시작합니다!")
    print("엔터를 누르면 녹음 시작 → 다시 엔터를 누르면 응답을 들을 수 있어요.")

    while True:
        filename = f"recordings/record_{uuid.uuid4().hex[:6]}.wav"
        record_until_enter(filename)
        text = transcribe(filename)

        if text.strip():
            if "요약" in text:
                from storage.db import get_recent_logs

                logs = get_recent_logs(days=7)
                log_text = "\n".join([f"- {log[2]}" for log in logs]) or "최근 기록이 없어요."

                prompt = f"다음은 최근 1주일 간의 아기 성장 기록입니다:\n{log_text}\n이 내용을 부모님께 요약해서 따뜻하게 말해 주세요."
                summary = get_gpt_response(prompt)
                speak(summary)
                continue

            if any(kw in text.lower() for kw in ["여기까지 마무리", "끝낼게"]):
                speak("알겠어요. 오늘도 수고 많으셨어요. 다음에 또 이야기해요 😊")
                break

            response = get_gpt_response(text)
            speak(response)
            # GPT 응답 끝난 뒤
            summary = get_log_summary_or_none(text)
            if summary:
                save_log(text, summary)
                print(f"📌 기록 저장됨: {summary}")
        else:
            print("❗ 아무 말도 인식되지 않았어요. 다시 시도해 주세요.")
