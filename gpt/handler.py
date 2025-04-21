import json
from openai import OpenAI
from config import BABY_NAME

client = OpenAI()


def analyze_user_input(user_input):
    prompt = f"""
사용자의 발화에 대해 아래 항목을 JSON 형식으로 응답하세요.

- "should_save": '{BABY_NAME}'의 성장, 감정, 건강, 식사, 수면 등과 관련된 내용이면 "YES", 그렇지 않으면 "NO"
- "summary": 저장할 경우 간결한 기록용 요약 문장, 저장하지 않는 경우 "NONE"
- "response": 짧고 따뜻한 공감 한 마디
- "tags": 관련 키워드 리스트 (예: 성장, 식사 등)
- "mood": 감정 키워드 리스트 (예: 기쁨, 감동 등)

사용자 발화:
{user_input}
"""

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    raw = completion.choices[0].message.content.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        print("⚠️ GPT 응답이 JSON 형식이 아님:", raw)
        return {
            "response": raw,
            "should_save": "NO",
            "summary": "NONE",
            "tags": [],
            "mood": []
        }


def summarize_logs(summaries: list[str]):
    if not summaries:
        return "최근 일주일 간의 기록이 없어요."

    joined = "\n".join(f"- {s}" for s in summaries)
    prompt = f"""
다음은 지난 1주일 간 아이의 성장 기록 요약입니다:

{joined}

이 내용을 부모님께 따뜻하게 전달하듯 요약해 주세요.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

