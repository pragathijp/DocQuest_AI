# DocQuest AI

AI-powered document question-answering system built using FastAPI, Qdrant, Gemini, and Retrieval-Augmented Generation (RAG).

## Overview

DocQuest AI allows users to upload PDF documents and ask natural language questions about their content. The system processes documents, generates embeddings, stores them in a vector database, retrieves relevant information, and uses a Large Language Model (LLM) to generate accurate answers with source references.

## Features

* PDF document upload and processing
* Text extraction and cleaning
* Intelligent text chunking
* Embedding generation using Sentence Transformers
* Semantic search using Qdrant
* Hybrid Retrieval (Qdrant + BM25)
* Retrieval-Augmented Generation (RAG)
* Conversational question answering with history support
* FastAPI REST APIs
* Automated testing using Pytest
* CI/CD using GitHub Actions
* Dependency monitoring with Dependabot
* Docker containerization support

## Tech Stack

### Backend

* Python
* FastAPI
* Pydantic

### AI / ML

* Google Gemini 2.5 Flash
* Sentence Transformers
* Retrieval-Augmented Generation (RAG)

### Vector Database

* Qdrant

### Retrieval

* Semantic Search
* BM25 Keyword Search
* Hybrid Retrieval

### DevOps

* GitHub Actions
* Dependabot
* Docker

### Testing

* Pytest
* HTTPX

## Project Structure

```text
DocQuest_AI/
├── app/
│   ├── indexing/
│   ├── retrieval/
│   └── main.py
├── tests/
├── docs/
│   └── screenshots/
├── .github/
│   ├── workflows/
│   └── dependabot.yml
├── requirements.txt
├── Dockerfile
└── Readme.md
```

## Architecture

```text
PDF Upload
    ↓
Text Extraction
    ↓
Cleaning
    ↓
Chunking
    ↓
Embedding Generation
    ↓
Qdrant Storage
    ↓
BM25 Indexing
    ↓
Hybrid Retrieval
    ↓
Reranking
    ↓
Gemini 2.5 Flash
    ↓
Answer + Sources + Confidence
```

## Local Setup

### Clone Repository

```bash
git clone https://github.com/pragathijp/DocQuest_AI.git
cd DocQuest_AI
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start Qdrant

```bash
docker run -p 6333:6333 qdrant/qdrant
```

### Configure Environment

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

### Run Application

```bash
uvicorn app.main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Workflow

1. Upload PDF document
2. Extract text from PDF
3. Clean and preprocess text
4. Generate text chunks
5. Create embeddings
6. Store vectors in Qdrant
7. Build BM25 index
8. Retrieve relevant chunks
9. Rerank retrieved results
10. Generate answer using Gemini
11. Return answer with sources and confidence score

## Screenshots

### Swagger API

![Swagger UI](docs/screenshots/swagger.png)

### Document Upload

![Upload](docs/screenshots/upload.png)

### Query Response

![Query](docs/screenshots/query.png)

## API Endpoints

### Upload Document

**POST** `/upload`

Uploads and indexes a PDF document.

### Query Document

**POST** `/query`

Queries an indexed document and returns an answer with supporting sources.

## CI/CD

The project includes:

* Automated testing with Pytest
* GitHub Actions workflow
* Dependency monitoring using Dependabot
* Docker container support

## Future Enhancements

* React frontend interface
* Cloud deployment (Google Cloud Run)
* Authentication and user management
* Multi-document querying
* Streaming responses
* Advanced analytics dashboard

## Author

**Pragathi J**
Computer Science Engineering Student
