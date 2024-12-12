# ingest.py

# ingest.py

import os
import shutil  # Import shutil for moving files
import box
import yaml
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.embeddings import HuggingFaceEmbeddings

# Import config vars
with open('config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))


def ingest_document(file_path):
    """
    Ingests a single PDF document by saving it to the data directory,
    splitting the text, creating embeddings, and updating the FAISS index.

    Args:
        file_path (str): Path to the PDF file to ingest.
    """
    # Ensure the data directory exists
    if not os.path.exists(cfg.DATA_PATH):
        os.makedirs(cfg.DATA_PATH)
        print(f"Created data directory at {cfg.DATA_PATH}")

    # Save the uploaded file to the data directory
    filename = os.path.basename(file_path)
    dest_path = os.path.join(cfg.DATA_PATH, filename)
    try:
        shutil.move(file_path, dest_path)  # Use shutil.move instead of os.rename
        print(f"Moved uploaded file to {dest_path}")
    except Exception as e:
        print(f"Error moving file: {e}")
        raise e

    # Load and split the document
    loader = PyPDFLoader(dest_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=cfg.CHUNK_SIZE,
        chunk_overlap=cfg.CHUNK_OVERLAP
    )
    texts = text_splitter.split_documents(documents)
    print(f"Split document into {len(texts)} chunks")

    # Create embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name=cfg.EMBEDDINGS,
        model_kwargs={'device': 'cpu'}
    )
    print("Created embeddings for the document")

    # Load existing FAISS index or create a new one
    if os.path.exists(cfg.DB_FAISS_PATH):
        vectorstore = FAISS.load_local(cfg.DB_FAISS_PATH, embeddings)
        print("Loaded existing FAISS index")
    else:
        vectorstore = FAISS.from_documents(texts, embeddings)
        print("Created new FAISS index")

    # Add new documents to the vectorstore
    vectorstore.add_documents(texts)
    print(f"Added {len(texts)} new documents to the FAISS index")

    # Save the updated FAISS index
    vectorstore.save_local(cfg.DB_FAISS_PATH)
    print(f"Saved FAISS index to {cfg.DB_FAISS_PATH}")


def run_ingest():
    """
    Ingests all PDF documents in the data directory.
    """
    loader = DirectoryLoader(
        cfg.DATA_PATH,
        glob='*.pdf',
        loader_cls=PyPDFLoader
    )

    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=cfg.CHUNK_SIZE,
        chunk_overlap=cfg.CHUNK_OVERLAP
    )
    texts = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name=cfg.EMBEDDINGS,
        model_kwargs={'device': 'cpu'}
    )

    vectorstore = FAISS.from_documents(texts, embeddings)
    vectorstore.save_local(cfg.DB_FAISS_PATH)


if __name__ == "__main__":
    run_ingest()

# import box
# import yaml
# from langchain.vectorstores import FAISS
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.document_loaders import PyPDFLoader, DirectoryLoader
# from langchain.embeddings import HuggingFaceEmbeddings
# 
# 
# # Import config vars
# with open('config.yml', 'r', encoding='utf8') as ymlfile:
#     cfg = box.Box(yaml.safe_load(ymlfile))
# 
# 
# def run_ingest():
#     loader = DirectoryLoader(cfg.DATA_PATH,
#                              glob='*.pdf',
#                              loader_cls=PyPDFLoader)
# 
#     documents = loader.load()
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=cfg.CHUNK_SIZE,
#                                                    chunk_overlap=cfg.CHUNK_OVERLAP)
#     texts = text_splitter.split_documents(documents)
# 
#     embeddings = HuggingFaceEmbeddings(model_name=cfg.EMBEDDINGS,
#                                        model_kwargs={'device': 'cpu'})
# 
#     vectorstore = FAISS.from_documents(texts, embeddings)
#     vectorstore.save_local(cfg.DB_FAISS_PATH)
# 
# if __name__ == "__main__":
#     run_ingest()

