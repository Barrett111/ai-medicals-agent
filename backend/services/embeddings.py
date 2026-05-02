from langchain_huggingface import HuggingFaceEmbeddings

def get_embeddings():
    print("🔄 Loading lightweight embeddings...")
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
