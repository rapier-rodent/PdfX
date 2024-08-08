import streamlit as st
import os
import json
import pandas as pd
from tempfile import NamedTemporaryFile

# You'll need to add these to requirements.txt later
from pypdf import PdfReader
from llama_index import SimpleDirectoryReader, GPTSimpleVectorIndex, LLMPredictor, PromptHelper, ServiceContext
from llama_index.llms import GeminiFamily

def extract_data_from_pdf(uploaded_file):
    """Extracts text content from the uploaded PDF file."""
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def create_json_from_text(text, gemini_api_key):
    """Interacts with the Gemini Pro API to structure the text into JSON."""

    llm_predictor = LLMPredictor(
        llm=GeminiFamily(
            api_key=gemini_api_key,
            model="gemini-pro",
            temperature=0,
            top_p=1.0,
            top_k=1
        )
    )
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

    prompt = f"""
    You are a helpful AI assistant that converts text to JSON. 
    The text to convert is delimited by triple backticks.
    ```
    {text}
    ```
    Return only the valid JSON output.
    """

    response = llm_predictor.predict(prompt)

    try:
        json_output = json.loads(response)
    except json.JSONDecodeError:
        st.error("The model did not return valid JSON. Please try again or adjust the prompt.")
        return None

    return json_output

def create_excel_from_json(json_data, file_name):
    """Creates an Excel file from the JSON data."""
    try:
        df = pd.DataFrame(json_data) 
    except ValueError:
        df = pd.json_normalize(json_data, sep='_') 

    with NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        df.to_excel(tmp.name, index=False)
        return tmp.name

def main():
    st.title("PDF to JSON/Excel Converter")

    gemini_api_key = st.secrets["GEMINI_API_KEY"]

    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        if st.button("Convert"):
            with st.spinner("Processing..."):
                extracted_text = extract_data_from_pdf(uploaded_file)
                json_output = create_json_from_text(extracted_text, gemini_api_key)

                if json_output:
                    st.download_button(
                        label="Download JSON",
                        data=json.dumps(json_output, indent=4),
                        file_name=uploaded_file.name.replace(".pdf", ".json"),
                        mime="application/json",
                    )

                    excel_file_path = create_excel_from_json(json_output, uploaded_file.name)
                    with open(excel_file_path, "rb") as f:
                        excel_data = f.read()
                    st.download_button(
                        label="Download Excel",
                        data=excel_data,
                        file_name=uploaded_file.name.replace(".pdf", ".xlsx"),
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )

if __name__ == "__main__":
    main()
