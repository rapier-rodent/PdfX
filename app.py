import streamlit as st
import pandas as pd
import fitz  # PyMuPDF
import json

# Function to read PDF and extract text
def extract_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(pdf_file) as pdf:
        for page in pdf:
            text += page.get_text()
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
        # Extract text from PDF
        pdf_text = extract_text_from_pdf(uploaded_file)

        # Convert text to JSON
        json_output = json.dumps({"transcription": pdf_text}, indent=4)

        # Save JSON to file
        json_filename = "transcription_output.json"
        with open(json_filename, "w") as json_file:
            json_file.write(json_output)

        # Save data to Excel
        excel_filename = "transcription_output.xlsx"
        save_to_excel({"transcription": [pdf_text]}, excel_filename)

        # Provide download links
        st.success("Transcription completed!")
        st.download_button("Download JSON", json_filename, mime="application/json")
        st.download_button("Download Excel", excel_filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.error("Please upload a PDF file.")
