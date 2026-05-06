import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_documents(file_paths):
    """
    Loads documents from the given file paths using LangChain loaders.
    """
    documents = []
    for path in file_paths:
        ext = os.path.splitext(path)[1].lower()
        if ext == ".pdf":
            loader = PyPDFLoader(path)
        elif ext == ".txt":
            loader = TextLoader(path)
        elif ext == ".docx":
            loader = Docx2txtLoader(path)
        else:
            print(f"Unsupported file format for {path}")
            continue
        
        try:
            docs = loader.load()
            # Add metadata about filename
            for doc in docs:
                doc.metadata["filename"] = os.path.basename(path)
            documents.extend(docs)
        except Exception as e:
            print(f"Error loading {path}: {e}")
            
    return documents

def split_documents(documents, chunk_size=1000, chunk_overlap=200):
    """
    Splits documents into smaller chunks using RecursiveCharacterTextSplitter.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    return text_splitter.split_documents(documents)
