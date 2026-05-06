import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

if not GEMINI_API_KEY:
    # We warn rather than raise error to avoid crashing on import if someone is just checking code.
    print("WARNING: GEMINI_API_KEY is not set in environment.")

