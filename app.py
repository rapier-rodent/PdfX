import streamlit as st
import requests
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

# Function to call the Gemini API
def call_gemini_api(api_key, text):
    url = "https://api.gemini.com/v1/transcribe"  # Replace with the actual API endpoint
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "input": text,
        "temperature": 0,
        "safety": "minimum"
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Function to save data to Excel
def save_to_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

# Streamlit app
st.title("PDF Transcription to JSON and Excel")

api_key = st.text_input("Enter your Gemini API Key:", type="password")
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if st.button("Transcribe"):
    if api_key and uploaded_file:
        # Extract text from PDF
        pdf_text = extract_text_from_pdf(uploaded_file)

        # Call Gemini API
        transcription_result = call_gemini_api(api_key, pdf_text)

        # Convert result to JSON
        json_output = json.dumps(transcription_result, indent=4)

        # Save JSON to file
        json_filename = "transcription_output.json"
        with open(json_filename, "w") as json_file:
            json_file.write(json_output)

        # Save data to Excel
        excel_filename = "transcription_output.xlsx"
        save_to_excel(transcription_result, excel_filename)

        # Provide download links
        st.success("Transcription completed!")
        st.download_button("Download JSON", json_filename, mime="application/json")
        st.download_button("Download Excel", excel_filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.error("Please enter your API key and upload a PDF file.")
