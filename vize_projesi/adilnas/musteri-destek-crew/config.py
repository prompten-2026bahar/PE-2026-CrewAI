import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()


def get_llm() -> LLM:
    provider = os.getenv("LLM_PROVIDER", "ollama").lower()

    if provider == "ollama":
        return LLM(
            model=os.getenv("OLLAMA_MODEL", "gemma3:12b"),
            provider="openai",
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
            api_key="ollama",
        )
    elif provider == "openai":
        return LLM(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            api_key=os.getenv("OPENAI_API_KEY"),
        )
    elif provider == "anthropic":
        return LLM(
            model=os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001"),
            api_key=os.getenv("ANTHROPIC_API_KEY"),
        )
    else:
        raise ValueError(f"Bilinmeyen LLM_PROVIDER: {provider}. 'ollama', 'openai' veya 'anthropic' kullanın.")


llm = get_llm()
