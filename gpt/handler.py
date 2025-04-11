from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_gpt_response(text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "당신은 따뜻하고 부드러운 육아 도우미 포도입니다."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content


def get_log_summary_or_none(user_input):
    prompt = f"""
사용자가 다음과 같은 육아 관련 말을 했을 때, 이 내용이 아기의 성장 기록으로 저장할 만한 내용이라면 짧게 요약해서 출력하고,
기록할 만한 내용이 아니라면 "NONE"이라고만 답해주세요.

사용자 발화:
{user_input}
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    result = response.choices[0].message.content.strip()
    return None if result == "NONE" else result
