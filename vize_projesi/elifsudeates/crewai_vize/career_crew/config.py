import os
from crewai import LLM
from dotenv import load_dotenv

# .env dosyasındaki değişkenleri yükle
load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")  # "ollama" or "gemini"

# Ollama Settings
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Gemini Settings
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_KEY_HERE")
GEMINI_MODELS = [
    "gemini-1.5-flash", 
    "gemini-1.5-pro", 
    "gemini-2.0-flash-exp",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-2-flash",
    "gemini-2-flash-lite",
    "gemini-3-flash",
    "gemini-3.1-pro",
    "gemini-3.1-flash-lite",
    "gemma-3-1b",
    "gemma-3-4b",
    "gemma-3-12b",
    "gemma-3-27b"
]

# Directory Settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
INPUTS_DIR = os.path.join(BASE_DIR, "inputs")

# Ensure directories exist
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(INPUTS_DIR, exist_ok=True)

# App Settings
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

def get_llm(provider: str = None, model: str = None, api_key: str = None):
    """Returns correct LLM object based on provider and model parameters"""
    p = (provider or LLM_PROVIDER).lower()
    m = model or (GEMINI_MODEL if p == "gemini" else OLLAMA_MODEL)
    key = api_key or (GEMINI_API_KEY if p == "gemini" else None)

    if p == "gemini":
        return LLM(model=f"gemini/{m}", api_key=key)
    
    # Default to Ollama
    return LLM(
        model=f"ollama/{m}",
        base_url=OLLAMA_BASE_URL
    )

def get_active_model_name(provider: str = None, model: str = None):
    """Returns the name of the model being used"""
    p = (provider or LLM_PROVIDER).lower()
    return model or (GEMINI_MODEL if p == "gemini" else OLLAMA_MODEL)
