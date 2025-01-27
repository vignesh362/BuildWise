import os
import openai
from openai import OpenAI
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import base64

load_dotenv()

class LLM:
    def __init__(self, model="gpt-4"):
        self.model = model
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.embeddings_model = SentenceTransformer('all-MiniLM-L6-v2')

    def answer(self, prompt, temperature=0):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=temperature,
        )
        return response.choices[0].message.content

    def get_embeddings(self, text):
        return self.embeddings_model.encode(text)

    def analyse_img(self, image_path):
        try:
            with open(image_path, "rb") as image_file:
                response = self.client.chat.completions.create(
                    model="gpt-4-vision-preview",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "Analyze this image in detail."
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64.b64encode(image_file.read()).decode()}"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=500
                )

            return response.choices[0].message.content

        except Exception as e:
            return f"An error occurred: {e}"
