from langchain_community.vectorstores import FAISS
from backend.services.embeddings import get_embeddings

def load_vector_store():
    embeddings = get_embeddings()
    return FAISS.load_local(
        "vector_store",
        embeddings,
        allow_dangerous_deserialization=True
    )

def get_retriever():
    db = load_vector_store()
    return db.as_retriever(search_kwargs={"k": 3})

print("Loading vector store...")
