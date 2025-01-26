from pytesseract import image_to_string  # For OCR
from PIL import Image
import fitz  # For PDF processing
import pandas as pd
import os
import glob
from Pineconedb import PineconeVectorDB  # Assuming PineconeVectorDB is defined in db.py
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

# Initialize OpenAI LLM
llm = OpenAI(
    temperature=0.5,
    openai_api_key="YOUR_OPENAI_API_KEY"
)

# Define the prompt template for text analysis
prompt_template = PromptTemplate(
    input_variables=["text"],
    template="""
You are an advanced text analysis system. Analyze the following OCR-extracted text, correct minor errors, and preserve exact numerical data. Then produce exactly two paragraphs of output:

1) The first paragraph is a thorough summary of the main themes, critical information, and key findings.
2) The second paragraph contains a concise numerical analysis (values, measurements, dates, codes, identifiers).

*** IMPORTANT RULES ***
- Do not include headings, such as "Paragraph 1" or "Paragraph 2."
- Do not include any extra text, notes, disclaimers, or formatting like "Aligned and Cleaned Text:".
- Provide exactly two paragraphs in total. Nothing more.
- The first paragraph: thorough summary. The second paragraph: numerical analysis.
- Do not restate these instructions in your output.

TEXT TO ANALYZE:
{text}

FINAL OUTPUT (TWO PARAGRAPHS, NO HEADINGS, NO EXTRA TEXT):
"""
)

# Helper functions for file processing
def process_pdf(pdf_path):
    """Extract text from a PDF file using Tesseract OCR."""
    doc = fitz.open(pdf_path)
    extracted_text = ""
    for page_num in range(len(doc)):
        page = doc[page_num]
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        extracted_text += image_to_string(img)
    return extracted_text

def process_image(image_path):
    """Extract text from an image using Tesseract OCR."""
    return image_to_string(Image.open(image_path))

def process_text_file(file_path):
    """Read plain text from a text file."""
    with open(file_path, 'r') as f:
        return f.read()

def process_csv(file_path):
    """Extract data from a CSV file."""
    df = pd.read_csv(file_path)
    return df.to_string()

def process_excel(file_path):
    """Extract data from an Excel file."""
    df = pd.read_excel(file_path)
    return df.to_string()

def analyze_text(text):
    """Analyze text using the LLM with the defined prompt."""
    prompt = prompt_template.format(text=text)
    return llm(prompt)

# Initialize Pinecone VectorDB
pinecone_db = PineconeVectorDB()

def store_in_pinecone(text):
    """Store processed text in Pinecone."""
    pinecone_db.query(text)  # Replace with actual storing logic
    return "Data stored in Pinecone."

# Main processing logic
if __name__ == "__main__":
    input_directory = "path/to/your/input/directory"

    for file_path in glob.glob(os.path.join(input_directory, "*")):
        try:
            print(f"Processing file: {file_path}")

            # Step 1: Process the file based on its type
            if file_path.endswith(".pdf"):
                extracted_data = process_pdf(file_path)
            elif file_path.endswith((".jpg", ".png", ".jpeg")):
                extracted_data = process_image(file_path)
            elif file_path.endswith(".txt"):
                extracted_data = process_text_file(file_path)
            elif file_path.endswith(".csv"):
                extracted_data = process_csv(file_path)
            elif file_path.endswith((".xls", ".xlsx")):
                extracted_data = process_excel(file_path)
            else:
                print(f"Unsupported file type: {file_path}")
                continue

            # Step 2: Analyze the extracted data
            analyzed_data = analyze_text(extracted_data)

            # Step 3: Store the analyzed data in Pinecone
            storage_result = store_in_pinecone(analyzed_data)

            print(f"Processed Output:\n{analyzed_data}")
            print(f"Storage Result: {storage_result}")

        except Exception as e:
            print(f"Error processing {file_path}: {e}")