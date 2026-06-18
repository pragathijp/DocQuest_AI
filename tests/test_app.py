import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_upload_rejects_non_pdf():
    response = client.post(
        "/upload", files={"file": ("notes.txt", b"hello world", "text/plain")}
    )
    assert response.status_code == 400
    assert "Only PDF files are supported" in response.json()["detail"]


@patch("app.main.process_document")
def test_upload_accepts_pdf(mock_process_document):
    mock_process_document.return_value = {"doc_id": "abc123", "status": "indexed"}
    response = client.post(
        "/upload",
        files={"file": ("report.pdf", b"%PDF-1.4 fake content", "application/pdf")},
    )
    assert response.status_code == 200
    assert response.json()["doc_id"] == "abc123"
    mock_process_document.assert_called_once()


@patch("app.main.process_document")
def test_upload_handles_processing_error(mock_process_document):
    mock_process_document.side_effect = ValueError("Could not parse PDF")
    response = client.post(
        "/upload",
        files={"file": ("broken.pdf", b"%PDF-1.4 corrupt", "application/pdf")},
    )
    assert response.status_code == 422
    assert "Could not parse PDF" in response.json()["detail"]


@patch("app.main.process_query")
def test_query_returns_contract_shape(mock_process_query):
    mock_process_query.return_value = {
        "answer": "This document is about AI/ML.",
        "sources": [{"page": 1, "text": "..."}],
        "confidence": 0.92,
    }
    response = client.post(
        "/query", json={"query": "What is this document about?", "doc_id": "abc123"}
    )
    assert response.status_code == 200
    body = response.json()
    assert "answer" in body and "sources" in body and "confidence" in body
    assert body["confidence"] > 0
    assert len(body["sources"]) > 0


@patch("app.main.process_query")
def test_query_fallback_when_no_chunks_found(mock_process_query):
    mock_process_query.return_value = {
        "answer": "No relevant info found",
        "sources": [],
        "confidence": 0,
    }
    response = client.post(
        "/query", json={"query": "irrelevant gibberish question", "doc_id": "abc123"}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["answer"] == "No relevant info found"
    assert body["sources"] == []
    assert body["confidence"] == 0


@patch("app.main.process_query")
def test_query_passes_history_correctly(mock_process_query):
    mock_process_query.return_value = {"answer": "Sure.", "sources": [], "confidence": 0.5}
    response = client.post(
        "/query",
        json={
            "query": "And what else?",
            "doc_id": "abc123",
            "history": [
                {"role": "user", "content": "What is this about?"},
                {"role": "assistant", "content": "AI."},
            ],
        },
    )
    assert response.status_code == 200
    called_history = mock_process_query.call_args[0][2]
    assert called_history == [
        {"role": "user", "content": "What is this about?"},
        {"role": "assistant", "content": "AI."},
    ]