import streamlit as st
import pandas as pd
import fitz  # PyMuPDF
import json
import pytesseract

# Function to read PDF and extract text using Tesseract
def extract_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(pdf_file) as pdf:
        for page in pdf:
            img = page.get_pixmap()
            text += pytesseract.image_to_string(img)
    return text

# Function to save data to Excel
def save_to_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

# Streamlit app
st.title("PDF Transcription to JSON and Excel")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if st.button("Transcribe"):
    if uploaded_file:
        # Extract text from PDF using Tesseract
        pdf_text = extract_text_from_pdf(uploaded_file)

        # Convert text to JSON
        json_output = json.dumps({"transcription": pdf_text}, indent=4)

        # Save JSON to file
        json_filename = "transcription_output.json"
        with
