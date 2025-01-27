import openai
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import base64
load_dotenv()

class LLM:
    def __init__(self, model="gpt-4"):
        self.model = model
        self.embeddings_model = SentenceTransformer('all-Mpnet-base-v2')
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": """You are a highly intelligent vision analysis system. Analyze the given image and provide the following:
1. If the image is a normal photo (e.g., scenery, objects, or people), describe the main objects, context, and overall scene in detail.
2. If the image contains a graph, chart, table, or similar visual representation of data, extract key numerical values, trends, and insights from the visual content.
3. Focus on providing concise, accurate descriptions or summaries, including any relevant numerical data for graphs or charts.

Image Analysis Instructions:
- For graphs or charts, identify axes labels, numerical ranges, peaks, troughs, and trends.
- For photos, describe objects, their relative positions, and any noticeable interactions or context.

Please analyze the image now."""
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


if __name__ == "__main__":
    llm = LLM()
    image_path = "path/to/your/image.png"  # Replace with your image file path

    # Analyze the image
    result = llm.analyse_img(image_path)
    print("Image Analysis Result:")
    print(result)
