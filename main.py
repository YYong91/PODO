from config import BABY_NAME
from utils.path import generate_recording_filename
from voice.input import record_until_enter, transcribe
from voice.output import speak
from gpt.handler import get_gpt_response, is_about_baby, get_conversational_response
from storage.db import init_db, save_log
from gpt.handler import get_log_summary_or_none

# 앱 시작 시 초기화
init_db()

if __name__ == "__main__":
    print("🍇 포도와 대화를 시작합니다!")
    print(f"예: 오늘 {BABY_NAME}가 혼자 앉았어 / 이번 주 요약해줘 / 마무리 / 끝낼게 / 그 외 기타 질문들")

    while True:
        filename = generate_recording_filename()
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

            if any(kw in text.lower() for kw in ["마무리", "끝낼게"]):
                speak("알겠어요. 오늘도 수고 많으셨어요. 다음에 또 이야기해요 😊")
                break

            about_baby = is_about_baby(text)
            if about_baby:
                # 기존 채이 관련 응답
                response = get_gpt_response(text)
            else:
                # 일반 궁금증 → 간단 or 자세히 처리
                response = get_conversational_response(text)
            speak(response)

            # GPT 응답 끝난 뒤
            if about_baby:
                summary = get_log_summary_or_none(text)
                if summary:
                    save_log(text, summary)
                    speak("기록할게요. 성장일지에 저장했어요 😊")
                    print(f"📌 기록 저장됨: {summary}")
            else:
                print("📝 일반 대화이므로 저장하지 않았어요.")
        else:
            print("❗ 아무 말도 인식되지 않았어요. 다시 시도해 주세요.")
