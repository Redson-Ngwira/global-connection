from groq import Groq
from django.conf import settings

client = Groq(api_key=settings.GROQ_API_KEY)

SYSTEM_PROMPT = (
    "You are an AI assistant replying via SMS. "
    "Keep answers short, clear, and under 500 characters. "
    "Use simple language. No markdown. No emojis."
)

def generate_reply(messages):
    chat = [{"role": "system", "content": SYSTEM_PROMPT}]

    # messages MUST be oldest → newest
    for m in messages:
        chat.append({
            "role": "assistant" if m.role == "assistant" else "user",
            "content": m.content
        })

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=chat,
        temperature=0.4,
        tools=[{"type":"browser_search"}],
        max_tokens=200
    )

    text = response.choices[0].message.content.strip()
    return text[:550]  # SMS safe
