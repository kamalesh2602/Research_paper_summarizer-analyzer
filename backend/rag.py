from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from backend.config import GEMINI_API_KEY, QDRANT_URL, QDRANT_API_KEY

COLLECTION_NAME = "research_papers_gemini"

class RAGPipeline:
    def __init__(self):
        # Initialize Embeddings exactly as requested
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-2",
            google_api_key=GEMINI_API_KEY
        )
        
        # Initialize Qdrant Client
        self.qdrant_client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
            timeout=60
        )
        
        self._ensure_collection()
        
        # Initialize LangChain Qdrant VectorStore
        self.vector_store = QdrantVectorStore(
            client=self.qdrant_client,
            collection_name=COLLECTION_NAME,
            embedding=self.embeddings,
        )

    def _ensure_collection(self):
        """Creates the Qdrant collection if it doesn't exist."""
        try:
            collections = self.qdrant_client.get_collections().collections
            if not any(c.name == COLLECTION_NAME for c in collections):
                # Using 3072 as the dimension for models/gemini-embedding-2
                self.qdrant_client.create_collection(
                    collection_name=COLLECTION_NAME,
                    vectors_config=VectorParams(size=3072, distance=Distance.COSINE),
                )
        except Exception as e:
            print(f"Error checking/creating collection: {e}")

    def add_documents(self, documents):
        """Adds LangChain Document objects to Qdrant."""
        if documents:
            self.vector_store.add_documents(documents)

    def get_retriever(self, k=5):
        """Returns a LangChain retriever interface."""
        return self.vector_store.as_retriever(search_kwargs={"k": k})

# Global instance so embeddings are loaded once
rag_pipeline = RAGPipeline()
