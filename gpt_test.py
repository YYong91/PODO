# gpt_test.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ask_gpt(message):
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}]
    )
    return chat_completion.choices[0].message.content


if __name__ == "__main__":
    print("포도와 대화를 시작합니다 🍇 (종료: ctrl+C)")
    while True:
        user_input = input("당신: ")
        reply = ask_gpt(user_input)
        print("포도: " + reply)
