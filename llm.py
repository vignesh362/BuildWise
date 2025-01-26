import os
from openai import OpenAI
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

class LLM:

    def __init__(self, model="gpt-4o"):
        self.model = model
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.embeddings_model = SentenceTransformer('all-Mpnet-base-v2')

    def answer(self, prompt, temperature=0):
        response = self.client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": prompt,
            }],
            model=self.model,
            temperature=temperature
        )
        return response.choices[0].message.content

    def get_embeddings(self, text):
        return self.embeddings_model.encode(text)
