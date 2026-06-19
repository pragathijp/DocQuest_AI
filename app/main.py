import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.indexing.pipeline import process_document
from app.retrieval.pipeline import process_query

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

app = FastAPI(title="DocQuest AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }


class HistoryMessage(BaseModel):
    role: str
    content: str


class QueryRequest(BaseModel):
    query: str
    doc_id: str
    history: list[HistoryMessage] = []


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File exceeds 20 MB limit."
        )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        result = process_document(tmp_path)

    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail=str(e)
        )

    finally:
        os.unlink(tmp_path)

    return result


@app.post("/query")
async def query(request: QueryRequest):
    history = [
        {
            "role": m.role,
            "content": m.content,
        }
        for m in request.history
    ]

    try:
        result = process_query(
            request.query,
            request.doc_id,
            history,
        )

        return result

    except KeyError:
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to process query."
        )