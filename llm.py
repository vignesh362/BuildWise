import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class LLM:

    def __init__(self, model="gpt-4o"):
        self.model = model
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def answer(self, prompt):
        response = self.client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": prompt,
            }],
            model=self.model,
        )
        return response.choices[0].message.content
