import streamlit as st
import cohere
import fitz # An alias for the PyMuPDF library.


def pdf_to_documents(pdf_path):
    """
    Converts a PDF to a list of 'documents' which are chunks of a larger document that can be easily searched
    and processed by the Cohere LLM. Each 'document' chunk is a dictionary with a 'title' and 'snippet' key

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        list: A list of dictionaries representing the documents. Each dictionary has a 'title' and 'snippet' key.
        Example return value: [{"title": "Page 1 Section 1", "snippet": "Text snippet..."}, ...]
    """

    doc = fitz.open(pdf_path)
    documents = []
    text = ""
    chunk_size = 1000
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        part_num = 1
        for i in range(0, len(text), chunk_size):
            documents.append({"title": f"Page {page_num + 1} Part {part_num}", "snippet": text[i:i + chunk_size]})
            part_num += 1
    return documents


api_key_found = False
if hasattr(st, "secrets"):
    if "COHERE_API_KEY" in st.secrets.keys():
        if st.secrets["COHERE_API_KEY"] not in ["", "PASTE YOUR API KEY HERE"]:
            api_key_found = True

# Add a sidebar to the Streamlit app
with st.sidebar:
    if api_key_found:
        cohere_api_key = st.secrets["COHERE_API_KEY"]
        # st.write("API key found.")
    else:
        cohere_api_key = st.text_input("Cohere API Key", key="chatbot_api_key", type="password")
        st.markdown("[Get a Cohere API Key](https://dashboard.cohere.ai/api-keys)")

    selected_doc = st.selectbox("Select Your Unit", ["1.1", "1.2", "2.1", "2.2"])