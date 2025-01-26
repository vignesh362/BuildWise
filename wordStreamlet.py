import streamlit as st
from fpdf import FPDF
from PIL import Image
import sys

# Hardcoded image path (e.g., a company logo)
HARDCODED_IMAGE_PATH = "nyu.png"

# Read arguments from the temporary file
if len(sys.argv) > 1:
    args_file = sys.argv[-1]
    with open(args_file, "r") as f:
        lines = f.readlines()
        initial_text = lines[0].strip()
        dynamic_image_path = lines[1].strip()
        title = lines[2].strip() if len(lines) > 2 else "Document Title"
else:
    initial_text = "This is the initial text to be displayed in the document."
    dynamic_image_path = ""
    title = "Document Title"

# Streamlit App
st.title("Dynamic Text and Image PDF Generator")

# Display the title
st.write("### Editable Title")
doc_title = st.text_input("Document Title:", value=title)

# Display the editable text
st.write("### Editable Document Content")
doc_text = st.text_area(
    "Document Content:",
    value=initial_text,
    height=300,
    key="doc_text_area",
)

# Display the dynamic image for content
st.write("### Image to Include Below Content in the PDF")
if dynamic_image_path:
    try:
        dynamic_image = Image.open(dynamic_image_path)
        st.image(dynamic_image, caption="Dynamic Content Image", use_container_width=False, width=400)
    except Exception as e:
        st.error(f"Error loading image from path: {dynamic_image_path}. Details: {e}")

# Display the hardcoded header image (preview only)
st.write("### Hardcoded Header Image Preview")
try:
    header_image = Image.open(HARDCODED_IMAGE_PATH)
    st.image(header_image, caption="Hardcoded Header Image (e.g., Company Logo)", use_container_width=False, width=200)
except Exception as e:
    st.error(f"Error loading hardcoded header image. Please check the path. Details: {e}")

# Create a container for the PDF generation and download
pdf_container = st.container()

# PDF generation and download
if st.button("Generate PDF"):
    try:
        pdf = FPDF()
        pdf.add_page()

        # Add the hardcoded header image
        try:
            pdf.image(HARDCODED_IMAGE_PATH, x=10, y=8, w=30)
        except Exception as e:
            st.error(f"Could not add hardcoded header image to PDF. Error: {e}")

        # Add the title
        pdf.set_font("Arial", size=16, style="B")
        pdf.cell(200, 10, txt=doc_title, ln=True, align="C")

        # Add some space below the title
        pdf.ln(10)

        # Add the document text
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, doc_text)

        # Add the dynamic image below the content
        if dynamic_image_path:
            try:
                pdf.add_page()
                pdf.image(dynamic_image_path, x=10, y=50, w=180)
            except Exception as e:
                st.error(f"Could not add dynamic content image to PDF. Error: {e}")

        # Save the PDF to a file
        pdf_file_path = "generated_document_with_images.pdf"
        pdf.output(pdf_file_path)

        # Display the download button in the container
        with pdf_container:
            with open(pdf_file_path, "rb") as pdf_file:
                st.download_button(
                    label="Download Generated PDF",
                    data=pdf_file,
                    file_name="generated_document_with_images.pdf",
                    mime="application/pdf",
                )
    except Exception as e:
        st.error(f"Error generating PDF: {e}")
