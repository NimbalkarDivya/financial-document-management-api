from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import os

from app.database import get_db
from app.models import Document
from app.dependencies import get_current_user
from app.utils import save_file

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload")
def upload_document(
    title: str,
    company_name: str,
    document_type: str,
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    file_path = f"uploads/{file.filename}"

    save_file(file, file_path)

    new_document = Document(
        title=title,
        company_name=company_name,
        document_type=document_type,
        file_path=file_path,
        uploaded_by=current_user,
        created_at=datetime.utcnow()
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return {
        "message": "Document uploaded",
        "document_id": new_document.id
    }


@router.get("/")
def get_documents(
    db: Session = Depends(get_db)
):

    return db.query(Document).all()


@router.get("/{document_id}")
def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):

    document = db.query(Document).filter(Document.id == document_id).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    return document


@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db)
):

    document = db.query(Document).filter(Document.id == document_id).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    os.remove(document.file_path)

    db.delete(document)
    db.commit()

    return {"message": "Document deleted"}