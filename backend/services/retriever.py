from langchain_community.vectorstores import FAISS
from backend.services.embeddings import get_embeddings
def load_vector_store():
    print("🔄 Loading vector store...")
    embeddings = get_embeddings()

    db = FAISS.load_local(
        "backend/vector_store",
        embeddings,
        allow_dangerous_deserialization=True
    )

    print("✅ Vector store loaded")
    return db