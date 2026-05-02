print("🔥 NEW EMBEDDINGS FILE LOADED")

from langchain_huggingface import HuggingFaceEmbeddings

def get_embeddings():
    print("✅ USING NEW IMPORT")
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
