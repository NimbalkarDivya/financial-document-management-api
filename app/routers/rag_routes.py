from fastapi import APIRouter
from PyPDF2 import PdfReader

from app.rag.chunking import chunk_text
from app.rag.vector_store import add_chunks, search_chunks
from app.schemas import SearchQuery

router = APIRouter(prefix="/rag", tags=["RAG"])


@router.post("/index-document")
def index_document(file_path: str):

    text = ""

    reader = PdfReader(file_path)

    for page in reader.pages:
        text += page.extract_text()

    chunks = chunk_text(text)

    add_chunks(chunks)

    return {"message": "Document indexed successfully"}


@router.post("/search")
def semantic_search(query: SearchQuery):

    results = search_chunks(query.query)

    return results