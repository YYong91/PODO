from openai import OpenAI
from dotenv import load_dotenv
import os

from config import BABY_NAME

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


def is_about_baby(text):
    prompt = f"""
사용자의 발화가 '{BABY_NAME}'라는 아이의 성장, 상태, 식사, 감정 등과 관련된 이야기라면 "YES"라고만 답하고,
그 외 일반적인 질문이나 일상 대화면 "NO"라고만 답하세요.

입력:
{text}
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    result = response.choices[0].message.content.strip().upper()
    return result == "YES"


def get_conversational_response(text):
    """
    사용자의 질문에 간단히 대답하되, '자세히' 요청이 있으면 자세히 설명
    """
    base_prompt = "사용자의 질문에 간단하고 핵심적인 답변을 해 주세요."
    if any(kw in text for kw in ["자세히", "상세하게", "더 알려줘"]):
        base_prompt = "사용자의 질문에 자세하고 구체적인 답변을 해 주세요."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": base_prompt},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content


def get_short_empathetic_response(user_input):
    # 예: GPT에게 짧은 공감 표현 요청
    prompt = f"""
사용자의 다음 말을 듣고, 성장 기록으로 저장하는 상황입니다.
따뜻하고 짧은 한 문장으로 공감 표현을 해 주세요.

입력:
{user_input}
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
