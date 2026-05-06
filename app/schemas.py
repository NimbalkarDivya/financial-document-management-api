from pydantic import BaseModel
from typing import Optional


class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class DocumentResponse(BaseModel):
    id: int
    title: str
    company_name: str
    document_type: str
    uploaded_by: str

    class Config:
        orm_mode = True


class SearchQuery(BaseModel):
    query: str