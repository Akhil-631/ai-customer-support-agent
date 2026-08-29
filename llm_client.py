import os
import time

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


client=OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
)

def call_llm(system_message, user_message):

    max_attempts = 3

    for attempt in range(1, max_attempts + 1):

        try:

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

        except Exception as e:

            print(
                f"\nLLM API attempt "
                f"{attempt}/{max_attempts} failed"
            )

            print(e)

            if attempt == max_attempts:

                raise
            
            time.sleep(1)
            
                