from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
import os
import shutil

from backend.loaders import load_documents, split_documents
from backend.rag import rag_pipeline
from backend.agents import run_summarizer_agent, run_analyzer_agent, run_chat_agent
from pydantic import BaseModel

app = FastAPI(title="Research Paper Analyzer API")

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class ChatRequest(BaseModel):
    query: str

@app.get("/debug")
async def debug_info():
    from backend.config import GEMINI_API_KEY
    return {"key": GEMINI_API_KEY[:10] + "..." if GEMINI_API_KEY else None}

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
        
    saved_paths = []
    
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_paths.append(file_path)
        
    try:
        # Load and split
        docs = load_documents(saved_paths)
        chunks = split_documents(docs)
        
        # Add to vector store
        rag_pipeline.add_documents(chunks)
        
        # Cleanup temp files
        for path in saved_paths:
            os.remove(path)
            
        return {"message": f"Successfully processed and embedded {len(files)} files.", "chunks_count": len(chunks)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/summarize")
async def summarize():
    try:
        result = run_summarizer_agent()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analyze")
async def analyze():
    try:
        result = run_analyzer_agent()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        result = run_chat_agent(request.query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Welcome to the Research Paper RAG API"}
