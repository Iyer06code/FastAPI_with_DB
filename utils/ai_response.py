import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

endpoint = "https://models.github.ai/inference"
model = "gpt-4o-mini"
load_dotenv()
token = os.environ["GITHUB_TOKEN"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

def get_completion(user_message, system_message="You are a helpful assistant.", history=None):
    """
    Get a completion from the AI model with optional conversation history.
    """

    if history is None:
        history = []

    messages = [
        SystemMessage(system_message)
    ]

    # Add previous conversation
    for msg in history:
        if msg["role"] == "user":
            messages.append(UserMessage(msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(SystemMessage(msg["content"]))

    # Add current user message
    messages.append(UserMessage(user_message))

    response = client.complete(
        messages=messages,
        model=model
    )

    return response.choices[0].message.content



