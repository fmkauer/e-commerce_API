from typing import List
from openai import OpenAI
import os
from src.schemas import ChatMessage


def generate_answer(user_id: int, messages: List[ChatMessage]) -> List[ChatMessage]:
    if messages[0].role != "system":
        messages.insert(
            0,
            ChatMessage(
                role="system",
                content="You are a helpful customer support agent of an e-commerce website.",
            ),
        )
    client = OpenAI(
        api_key=os.getenv("API_KEY"),
        base_url=os.getenv("PROXY_URL"),
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )
    messages.append(
        ChatMessage(
            role="assistant",
            content=response.choices[0].message.content,
        )
    )
    return messages


if __name__ == "__main__":
    user_id = None
    messages = []
    while True:
        if not user_id:
            user_id = int(input("Enter user id: "))
        message = input("Enter message (or 'q' to quit):\n")
        if message == "q":
            print("Quitting...")
            break
        messages.append({"role": "user", "content": message})
        messages = generate_answer(user_id, messages)
        print("Assistant: ", messages[-1].content)
