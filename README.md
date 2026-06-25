# Research Paper Summarizer & Analyzer using RAG

## Overview

A Retrieval-Augmented Generation (RAG) application for summarizing and analyzing research papers. The project uses:

* **FastAPI** – Backend API
* **Streamlit** – Frontend UI
* **Qdrant** – Vector Database
* **Google Gemini** – Embeddings & LLM

---

# Setup

## 1. Clone the repository

```bash
git clone https://github.com/kamalesh2602/Research_paper_summarizer-analyzer
cd Research_paper_summarizer-analyzer
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Copy the example environment file.

```bash
cp .env.example .env
```

(or create `.env` manually on Windows.)

Update the values accordingly.

### Option A – Qdrant Cloud

```env
GEMINI_API_KEY=your_gemini_api_key

QDRANT_URL=https://your-cluster.cloud.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key
```

### Option B – Local Qdrant using Docker

```env
GEMINI_API_KEY=your_gemini_api_key

QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=
```

> Leave `QDRANT_API_KEY` empty when using a local Docker instance.

---

## 5. Start Qdrant

### Option A – Qdrant Cloud

No additional setup is required. Ensure your `.env` contains the correct Cloud URL and API key.

---

### Option B – Local Docker

Make sure Docker Desktop is installed and running.

```bash
docker run -d \
  --name qdrant \
  -p 6333:6333 \
  -v qdrant_storage:/qdrant/storage \
  qdrant/qdrant
```

Verify that Qdrant is running:

```bash
docker ps
```

You can also access the dashboard at:

```
http://localhost:6333/dashboard
```

---

## 6. Run the Backend

```bash
uvicorn backend.main:app --reload
```

---

## 7. Run the Frontend

```bash
streamlit run frontend/app.py
```

---

## Project Structure

```
backend/
frontend/
data/
uploads/
.env
requirements.txt
README.md
```
