import os

from App.services.groq_modules.groq_client import client

def search_model(prompt, his=None):
    messages = []
    if his is not None:
        messages.extend(his)

    messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    completion = client.chat.completions.create(
        model="compound-beta",
        messages=messages
    )

    return completion.choices[0].message.content
# Print all tool calls
# print(completion.choices[0].message.executed_tools)
