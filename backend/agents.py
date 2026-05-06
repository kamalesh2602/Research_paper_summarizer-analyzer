from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from backend.rag import rag_pipeline
from backend.config import GEMINI_API_KEY
import json

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.2,
    convert_system_message_to_human=True
)

def _get_context(query: str, k: int = 5) -> str:
    retriever = rag_pipeline.get_retriever(k=k)
    docs = retriever.invoke(query)
    context = "\n\n".join([f"Source ({d.metadata.get('filename', 'Unknown')}):\n{d.page_content}" for d in docs])
    return context

def run_summarizer_agent():
    """
    Summarizes the documents in the DB into specific sections.
    """
    # General query to get a broad overview of the documents
    context = _get_context("Give me a comprehensive overview of the research paper including methodology and findings.", k=10)
    
    prompt = PromptTemplate(
        template="""You are an expert Research Paper Summarizer. Based on the provided context, generate a structured summary.
        
        Context:
        {context}
        
        Output format: Return ONLY a valid JSON object with the following keys exactly:
        - "Title": (Infer title if possible, otherwise write "Unknown Title")
        - "Abstract": (A brief summary of what the paper is about)
        - "Methodology": (How the research was conducted)
        - "Key Findings": (The main results and discoveries)
        - "Conclusion": (The final conclusions drawn by the authors)
        """,
        input_variables=["context"]
    )
    
    chain = prompt | llm
    response = chain.invoke({"context": context})
    
    try:
        # Strip markdown json block formatting if present
        content = response.content.strip()
        if content.startswith("```json"):
            content = content[7:-3]
        elif content.startswith("```"):
            content = content[3:-3]
        return json.loads(content)
    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON", "raw": response.content}

def run_analyzer_agent():
    """
    Analyzes the documents in the DB for strengths, weaknesses, etc.
    """
    context = _get_context("What are the strengths, weaknesses, limitations, and novel aspects of the research?", k=10)
    
    prompt = PromptTemplate(
        template="""You are an expert Research Paper Analyzer. Based on the provided context, critically analyze the paper.
        
        Context:
        {context}
        
        Output format: Return ONLY a valid JSON object with the following keys exactly:
        - "Strengths": (List of strong points of the research)
        - "Weaknesses": (List of weak points or flaws)
        - "Novelty": (What is new or innovative about this research)
        - "Limitations": (Stated or implied limitations of the study)
        - "Suggestions": (Future work or suggestions for improvement)
        """,
        input_variables=["context"]
    )
    
    chain = prompt | llm
    response = chain.invoke({"context": context})
    
    try:
        content = response.content.strip()
        if content.startswith("```json"):
            content = content[7:-3]
        elif content.startswith("```"):
            content = content[3:-3]
        return json.loads(content)
    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON", "raw": response.content}

def run_chat_agent(query: str):
    """
    Answers user queries based on the document context.
    """
    context = _get_context(query, k=5)
    
    prompt = PromptTemplate(
        template="""You are a helpful AI assistant that answers questions about research papers.
        Use ONLY the following context to answer the user's question. If you cannot answer based on the context, say so.
        
        Context:
        {context}
        
        Question:
        {query}
        
        Answer:""",
        input_variables=["context", "query"]
    )
    
    chain = prompt | llm
    response = chain.invoke({"context": context, "query": query})
    return {"response": response.content, "context_used": context}
