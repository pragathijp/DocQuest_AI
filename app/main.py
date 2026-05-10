import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.indexing.pipeline import process_document
from app.retrieval.pipeline import process_query

app = FastAPI(title="DocQuest AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str
    doc_id: str

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    try:
        result = process_document(tmp_path)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    finally:
        os.unlink(tmp_path)
    return result

@app.post("/query")
async def query(request: QueryRequest):
    result = process_query(request.query, request.doc_id)
    return result