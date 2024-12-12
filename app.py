# app.py

import streamlit as st
import tempfile
import os
import shutil  # Import shutil if needed elsewhere
from ingest import ingest_document
from main import get_answer

# Load configuration
import box
import yaml

with open('config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))

# Streamlit App Title
st.title("📄 LLM RAG Pipeline Dashboard")

# Sidebar for uploading PDF
st.sidebar.header("Upload PDF Document")
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type=["pdf"])

# Option to perform semantic search
semantic_search = st.sidebar.checkbox("Enable Semantic Search", value=False)

# Input for query
st.header("🔍 Enter Your Query")
query = st.text_input("Type your query here")

# Button to submit the query
if st.button("Submit Query"):
    if uploaded_file is not None and query.strip() != "":
        with st.spinner("Ingesting the document..."):
            try:
                # Save the uploaded file to a temporary directory
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_file_path = tmp_file.name
                    st.write(f"Temporary file created at {tmp_file_path}")  # Debugging statement

                # Check if the temp file exists
                if not os.path.exists(tmp_file_path):
                    st.error("Temporary file was not created successfully.")
                    st.stop()

                # Ingest the document
                ingest_document(tmp_file_path)
                st.success("Document ingested successfully!")

                # Remove the temporary file if it still exists
                if os.path.exists(tmp_file_path):
                    os.remove(tmp_file_path)
                    st.write("Temporary file removed.")
            except Exception as e:
                st.error(f"Error during ingestion: {e}")
                st.stop()

        with st.spinner("Processing your query..."):
            try:
                answer, time_taken = get_answer(query, semantic_search=semantic_search)
                st.success(f"Query processed successfully in {time_taken:.2f} seconds!")
                st.write("### Answer:")
                st.write(answer)
            except Exception as e:
                st.error(f"Error processing query: {e}")
    else:
        st.error("Please upload a PDF and enter a query.")
