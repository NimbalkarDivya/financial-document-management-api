from fastapi import FastAPI

from app.database import Base, engine

from app.routers.auth_routes import router as auth_router
from app.routers.document_routes import router as document_router
from app.routers.role_routes import router as role_router
from app.routers.rag_routes import router as rag_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(document_router)
app.include_router(role_router)
app.include_router(rag_router)


@app.get("/")
def home():
    return {"message": "Financial Document API Running"}