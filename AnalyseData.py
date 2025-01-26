from langchain import PromptTemplate, LLMChain
from langchain.llms import OpenAI
from langchain.agents import Tool, initialize_agent, AgentType
from pytesseract import image_to_string  # For OCR
from PIL import Image
import fitz  # For PDF processing
import pandas as pd
import os
import glob
from db import PineconeVectorDB  # Assuming PineconeVectorDB is defined in db.py

# Initialize OpenAI LLM
llm = OpenAI(
    temperature=0.7,
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

# Define helper functions for different file types
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
    """Extract text from an image using a vision LLM (mocked here)."""
    # Replace with a call to a vision LLM model
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

# Initialize Pinecone VectorDB
pinecone_db = PineconeVectorDB()

def store_in_pinecone_tool(text):
    """Store processed text in Pinecone."""
    pinecone_db.query(text)  # Replace with actual storing logic if necessary
    return "Data stored in Pinecone."

# Define tools for the agent
process_pdf_tool = Tool(
    name="ProcessPDF",
    func=process_pdf,
    description="Extracts text from a PDF file using Tesseract OCR."
)

process_image_tool = Tool(
    name="ProcessImage",
    func=process_image,
    description="Extracts text from an image file using a vision model."
)

process_text_tool = Tool(
    name="ProcessText",
    func=process_text_file,
    description="Reads plain text from a text file."
)

process_csv_tool = Tool(
    name="ProcessCSV",
    func=process_csv,
    description="Extracts data from a CSV file as plain text."
)

process_excel_tool = Tool(
    name="ProcessExcel",
    func=process_excel,
    description="Extracts data from an Excel file as plain text."
)

analyze_text_tool = Tool(
    name="AnalyzeText",
    func=lambda text: LLMChain(llm=llm, prompt=prompt_template).run({"text": text}),
    description="Analyzes text using an advanced LLM to correct, summarize, and extract numerical data."
)

store_text_tool = Tool(
    name="StoreTextInPinecone",
    func=store_in_pinecone_tool,
    description="Stores the processed text in the Pinecone vector database."
)

# Define the agent
agent = initialize_agent(
    tools=[
        process_pdf_tool,
        process_image_tool,
        process_text_tool,
        process_csv_tool,
        process_excel_tool,
        analyze_text_tool,
        store_text_tool
    ],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

if __name__ == "__main__":
    # Directory containing files
    input_directory = "path/to/your/input/directory"

    # Process all files in the directory
    for file_path in glob.glob(os.path.join(input_directory, "*")):
        try:
            print(f"Processing file: {file_path}")
            output = agent.run(file_path)
            print(f"Processed Output:\n{output}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")