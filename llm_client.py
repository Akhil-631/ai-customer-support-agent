import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


client=OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
)

def call_llm(system_message, user_message):

    response = client.chat.completions.create(

        model="openai/gpt-oss-20b",

        messages=[
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": user_message
            }
        ],

        temperature=0.0,
    )

    return response.choices[0].message.content.strip()
