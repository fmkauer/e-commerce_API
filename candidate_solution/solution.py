from typing import List, Dict, Any
from openai import OpenAI
import os
from src.schemas import ChatMessage
import requests


def get_jwt_token(username: str, password: str):
    response = requests.post(
        f"http://localhost:8000/login",
        data={"username": username, "password": password},
    )
    response.raise_for_status()
    return response.json()["access_token"]


def get_user_by_id(user_id: int, jwt_token: str):
    response = requests.get(
        f"http://localhost:8000/user/{user_id}",
        headers={"Authorization": f"Bearer {jwt_token}"},
    )
    return response.json()


def get_user_info(user_id: int) -> Dict[str, Any]:
    # For demonstration, we'll use a hardcoded token. In production, you should handle authentication properly
    jwt_token = get_jwt_token("admin", "admin123")
    user_data = get_user_by_id(user_id, jwt_token)
    return {"username": user_data["username"], "email": user_data["email"]}


def generate_answer(user_id: int, messages: List[ChatMessage]) -> List[ChatMessage]:
    if messages[0].role != "system":
        messages.insert(
            0,
            ChatMessage(
                role="system",
                content=f"You are a helpful customer support agent of an e-commerce website. You have access to user information through the get_user_info tool. The user_id is {user_id}",
            ),
        )

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_user_info",
                "description": "Get the username and email of the current user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "integer",
                            "description": "The ID of the user",
                        }
                    },
                    "required": ["user_id"],
                },
            },
        }
    ]

    client = OpenAI(
        api_key=os.getenv("API_KEY"),
        base_url=os.getenv("PROXY_URL"),
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=messages, tools=tools, tool_choice="auto"
    )

    assistant_message = response.choices[0].message

    if assistant_message.tool_calls:
        for tool_call in assistant_message.tool_calls:
            messages.append(
                ChatMessage(
                    role="assistant",
                    tool_calls=[
                        {
                            "id": tool_call.id,
                            "type": tool_call.type,
                            "function": {
                                "name": tool_call.function.name,
                                "arguments": tool_call.function.arguments,
                            },
                        }
                    ],
                )
            )
            if tool_call.function.name == "get_user_info":
                user_info = get_user_info(user_id)
                messages.append(
                    ChatMessage(
                        role="tool",
                        content=str(user_info),
                        tool_call_id=tool_call.id,
                        name=tool_call.function.name,
                    )
                )

        # Make a second call to process the tool response
        response = client.chat.completions.create(
            model="gpt-4o-mini", messages=messages
        )
        assistant_message = response.choices[0].message

    messages.append(
        ChatMessage(
            role="assistant",
            content=assistant_message.content,
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
        messages.append(ChatMessage(role="user", content=message))
        messages = generate_answer(user_id, messages)
        print("Assistant: ", messages[-1].content)
