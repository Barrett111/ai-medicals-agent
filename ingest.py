import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Load PDF
pdf_path = "data/documents/sample.pdf"

if not os.path.exists(pdf_path):
    print("❌ No PDF found. Add file in data/documents/")
    exit()

loader = PyPDFLoader(pdf_path)
documents = loader.load()

# Split text
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_documents(documents)

# Embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Vector DB
db = FAISS.from_documents(docs, embeddings)

# Save
db.save_local("vector_store")

print("✅ Documents embedded successfully!")