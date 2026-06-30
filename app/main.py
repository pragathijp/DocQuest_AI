
import os
import tempfile
from datetime import datetime

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException,
    Request,
)
from fastapi.middleware.cors import (
    CORSMiddleware
)
from fastapi.responses import (
    JSONResponse
)
from pydantic import (
    BaseModel,
    Field,
)

from app.config import CORS_ORIGINS
from app.qdrant_client import (
    client as qdrant_client
)

from app.indexing.pipeline import (
    process_document
)
from app.retrieval.pipeline import (
    process_query
)
from app.utils.logger import (
    get_logger
)

logger = get_logger(__name__)

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB


app = FastAPI(
    title="DocQuest AI",
    version="1.0.0",
    description=(
        "Production RAG system powered by "
        "Gemini, Qdrant, Hybrid Retrieval, "
        "BM25, RRF, and CrossEncoder reranking."
    ),
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# ==========================================
# Exception Handlers
# ==========================================

@app.exception_handler(
    HTTPException
)
async def http_exception_handler(
    request: Request,
    exc: HTTPException
):
    logger.warning(
        f"HTTP {exc.status_code} - "
        f"{request.method} {request.url} - "
        f"{exc.detail}"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    logger.exception(
        f"Unhandled exception during "
        f"{request.method} {request.url}"
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error"
        }
    )


# ==========================================
# Health Check
# ==========================================

@app.get(
    "/health",
    tags=["Monitoring"]
)
async def health():
    return {
        "status": "healthy",
        "timestamp": (
            datetime.utcnow()
            .isoformat()
        ),
    }


# ==========================================
# Readiness Check
# ==========================================

@app.get(
    "/readiness",
    tags=["Monitoring"]
)
async def readiness():
    try:
        qdrant_client.get_collections()

        return {
            "status": "ready"
        }

    except Exception as e:
        logger.warning(
            f"Readiness check failed: "
            f"{str(e)}"
        )

        raise HTTPException(
            status_code=503,
            detail=(
                "Qdrant is not reachable"
            ),
        )


# ==========================================
# Request Models
# ==========================================

class HistoryMessage(
    BaseModel
):
    role: str
    content: str


class QueryRequest(
    BaseModel
):
    query: str
    doc_id: str

    history: list[
        HistoryMessage
    ] = Field(
        default_factory=list
    )


# ==========================================
# Upload Endpoint
# ==========================================

@app.post(
    "/upload",
    tags=["Documents"]
)
async def upload(
    file: UploadFile = File(...)
):
    if not file.filename.endswith(
        ".pdf"
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                "Only PDF files "
                "are supported."
            ),
        )

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=(
                "File exceeds "
                "20 MB limit."
            ),
        )

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as tmp:
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        result = process_document(
            tmp_path
        )

        return result

    except ValueError as e:
        logger.exception(
            f"UPLOAD FAILED: {str(e)}"
        )
        raise HTTPException(
            status_code=422,
            detail=str(e),
        )

    except Exception as e:
        logger.exception(
            f"UPLOAD FAILED: {str(e)}"
        )
        raise

    finally:
        if os.path.exists(
            tmp_path
        ):
            os.unlink(
                tmp_path
            )
# ==========================================
# Query Endpoint
# ==========================================

@app.post(
    "/query",
    tags=["Retrieval"]
)
async def query(
    request: QueryRequest
):
    history = [
        {
            "role": m.role,
            "content": m.content,
        }
        for m in request.history
    ]

    try:
        return process_query(
            request.query,
            request.doc_id,
            history,
        )

    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=(
                "Document not found."
            ),
        )
