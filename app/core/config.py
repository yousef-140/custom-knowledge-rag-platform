from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2")

    TEMPERATURE = float(os.getenv("TEMPERATURE", 0.3))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", 512))

    TOP_K = int(os.getenv("TOP_K", 5))
    ALPHA = float(os.getenv("ALPHA", 0.5))

    MAX_CONTEXT_CHUNKS = int(os.getenv("MAX_CONTEXT_CHUNKS", 3))
    MAX_CONTEXT_CHARS = int(os.getenv("MAX_CONTEXT_CHARS", 2000))

    PDF_PATH = os.getenv("PDF_PATH", "data/raw/sf.pdf")
    INDEX_PATH = os.getenv("INDEX_PATH", "data/index.faiss")

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")


settings = Settings()