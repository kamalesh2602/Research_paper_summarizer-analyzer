# Research Paper Summarizer & Analyzer using RAG

## Overview
This project is a Research Paper Summarizer and Analyzer utilizing RAG. 
It uses FastAPI for the backend, Streamlit for the frontend, Qdrant as the vector database, and Gemini API for embeddings and language models.

## Setup

1. **Clone the repository.**
2. **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4. **Environment Variables:**
    - Copy `.env.example` to `.env` and fill in your `GEMINI_API_KEY` and Qdrant details.

5. **Run Qdrant:**
    - Assuming you have Docker installed:
    ```bash
    docker run -p 6333:6333 -p 6334:6334 -v $(pwd)/qdrant_storage:/qdrant/storage:z qdrant/qdrant
    ```

6. **Run Backend:**
    ```bash
    uvicorn backend.main:app --reload
    ```

7. **Run Frontend:**
    ```bash
    streamlit run frontend/app.py
    ```
