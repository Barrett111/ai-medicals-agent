from fastapi import APIRouter
from backend.models.schema import QueryRequest
from backend.services.rag_pipeline import get_answer

router = APIRouter()

@router.post("/")
def chat(request: QueryRequest):
    return get_answer(request.query)