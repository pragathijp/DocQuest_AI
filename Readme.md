# DocQuest AI

AI-powered document question-answering system built using FastAPI, Qdrant, Gemini, and Retrieval-Augmented Generation (RAG).

## Overview

DocQuest AI allows users to upload PDF documents and ask natural language questions about their content. The system processes documents, generates embeddings, stores them in a vector database, retrieves relevant information, and uses a Large Language Model (LLM) to generate accurate answers with source references.

## Features

* PDF document upload and processing
* Text extraction and chunking
* Vector embeddings generation
* Semantic search using Qdrant
* Retrieval-Augmented Generation (RAG)
* Conversational question answering with history support
* FastAPI backend APIs
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

* Google Gemini
* Sentence Transformers
* RAG Pipeline

### Vector Database

* Qdrant

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
├── .github/
│   ├── workflows/
│   └── dependabot.yml
├── requirements.txt
├── Dockerfile
└── Readme.md
```

## Workflow

1. Upload PDF document
2. Extract and clean text
3. Generate chunks
4. Create embeddings
5. Store vectors in Qdrant
6. Retrieve relevant chunks
7. Generate answer using Gemini
8. Return answer with sources and confidence

## CI/CD

The project includes:

* Automated testing with Pytest
* GitHub Actions workflow
* Dependency monitoring using Dependabot
* Docker container support

## Future Enhancements

* Frontend user interface
* Cloud deployment
* Authentication and user management
* Multi-document querying
* Advanced analytics dashboard

## Author

Pragathi J
Computer Science Engineering Student
